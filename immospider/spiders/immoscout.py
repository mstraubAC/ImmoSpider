# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
import json
from immospider.items import ImmoscoutItem


class ImmoscoutSpider(scrapy.Spider):
    name = "immoscout"
    allowed_domains = ["immobilienscout24.de"]
    # start_urls = ['https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin']
    # start_urls = ['https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin/Lichterfelde-Steglitz_Nikolassee-Zehlendorf_Dahlem-Zehlendorf_Zehlendorf-Zehlendorf/2,50-/60,00-/EURO--800,00/-/-/']

    # The immoscout search results are stored as json inside their javascript. This makes the parsing very easy.
    # I learned this trick from https://github.com/balzer82/immoscraper/blob/master/immoscraper.ipynb .
    script_xpath = './/script[contains(., "IS24.resultList")]'
    details_xpath = './/script[contains(., "keyValues")]'
    expose_xpath = './/script[contains(., "IS24.expose")]'
    next_xpath = '//div[@id = "pager"]/div/a/@href'

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse_expose(self, response):
        for line in response.xpath(self.details_xpath).extract_first().split('\n'):
            if line.strip().startswith('var keyValues'):
                details_json = line.strip()
                details_json = details_json[16:-1]
                details = json.loads(details_json)

                item = response.meta.get('thisItem')
                if 'obj_picturecount' in details:
                    item['pictureCount'] = details['obj_picturecount']
                if 'obj_pricetrend' in details:
                    item['priceTrend'] = details['obj_pricetrend']
                if 'obj_rented' in details:
                    item['rented'] = details['obj_rented']
    
                if 'obj_yearConstructed' in details:
                    item['yearConstructed'] = details['obj_yearConstructed']
                if 'obj_condition' in details:
                    item['condition'] = details['obj_condition']
                if 'obj_interiorQuality' in details:
                    item['interiorQuality'] = details['obj_interiorQuality']
                if 'obj_numberOfFloors' in details:
                    item['numberOfFloors'] = details['obj_numberOfFloors']
                if 'obj_buildingType' in details:
                    item['buildingType'] = details['obj_buildingType']

                if 'obj_heatingType' in details:
                    item['heatingType'] = details['obj_heatingType']
                if 'obj_firingType' in details:
                    item['heatingFiringType'] = details['obj_firingType']
                if 'obj_energyEfficiencyClass' in details:
                    item['energyEfficiencyClass'] = details['obj_energyEfficiencyClass']
    
                if 'obj_noParkSpaces' in details:
                    item['parkSpaces'] = details['obj_noParkSpaces']

                if 'obj_telekomDownloadSpeed' in details: 
                    item['telekomDownloadSpeed'] = details['obj_telekomDownloadSpeed']
                if 'obj_telekomUploadSpeed' in details: 
                    item['telekomUploadSpeed'] = details['obj_telekomUploadSpeed']
                if 'obj_telekomTechnology' in details: 
                    item['telekomTechnology'] = details['obj_telekomInternetTechnology']
                if 'obj_telekomInternetType' in details: 
                    item['telekomInternetType'] = details['obj_telekomInternetType']

                yield item

    def parse(self, response):

        print(response.url)

        for line in response.xpath(self.script_xpath).extract_first().split('\n'):
            if line.strip().startswith('resultListModel'):
                immo_json = line.strip()
                try:
                    immo_json = json.loads(immo_json[17:-1])
    
                    #TODO: On result pages with just a single result resultlistEntry is not a list, but a dictionary.
                    #TODO: So extracting data will fail.
                    numberOfHits = int(immo_json["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["@numberOfHits"])
                    print("Number of hits: %i" % ( numberOfHits, ))
                    for result in immo_json["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]:
    
                        item = ImmoscoutItem()
    
                        data = result["resultlist.realEstate"]
    
                        # print(data)
    
                        item['immo_id'] = data['@id']
                        item['createdAtDate'] = result['@creation']
                        item['modifiedAtDate'] = result['@modification']
                        item['publishedAtDate'] = result['@publishDate']
                        item['hasNewFlag'] = result['hasNewFlag']
                        item['url'] = response.urljoin("/expose/" + str(data['@id']))
                        item['title'] = data['title']
                        address = data['address']
                        try:
                            item['address'] = address['street'] + " " + address['houseNumber']
                        except:
                            item['address'] = None    
                        if 'newHomeBuilder' in result:
                            item['newHomeBuilder'] = result['newHomeBuilder']
                        else:
                            item['newHomeBuilder'] = None
                        if 'floorplan' in data:
                            item['floorplan'] = data['floorplan']
                        else:
                            item['floorplan'] = None
                        item['city'] = address['city']
                        item['zip_code'] = address['postcode']
                        item['district'] = address['quarter']
    
                        item["rent"] = data["price"]["value"]
                        item["livingSpace"] = data["livingSpace"] # Wohnflaeche
                        item["rooms"] = data["numberOfRooms"]
    
                        if "calculatedPrice" in data:
                            item["extra_costs"] = (data["calculatedPrice"]["value"] - data["price"]["value"])
                        if "builtInKitchen" in data:
                            item["kitchen"] = data["builtInKitchen"]
                        if "balcony" in data:
                            item["balcony"] = data["balcony"]
                        if "garden" in data:
                            item["garden"] = data["garden"]
                        if "privateOffer" in data:
                            item["private"] = data["privateOffer"]
                        if "plotArea" in data:
                            item["plotArea"] = data["plotArea"]
                        if "cellar" in data:
                            item["cellar"] = data["cellar"]       
    
                        try:
                            contact = data['contactDetails']
                            item['contact_name'] = contact['firstname'] + " " + contact["lastname"]
                        except:
                            item['contact_name'] = None
    
                        try:
                            item['media_count'] = len(data['galleryAttachments']['attachment'])
                        except:
                            item['media_count'] = 0
    
                        try:
                            item['lat'] = address['wgs84Coordinate']['latitude']
                            item['lng'] = address['wgs84Coordinate']['longitude']
                        except Exception as e:
                            # print(e)
                            item['lat'] = None
                            item['lng'] = None 
                        
#                        yield item
                        yield Request(item['url'], callback=self.parse_expose, meta={'thisItem': item})

                except Exception as e:
                    print("There was a general error: %s" % ( e, ))
                    #print("!!!! GENERAL ERROR !!!!"


        next_page_list = response.xpath(self.next_xpath).extract()
        if next_page_list:
            next_page = next_page_list[-1]
            print("Scraping next page", next_page)
            if next_page:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
