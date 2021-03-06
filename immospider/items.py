# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImmoscoutItem(scrapy.Item):
    # define the fields for your item here like:
    #  name = scrapy.Field()
    immo_id = scrapy.Field()
    createdAtDate = scrapy.Field()
    modifiedAtDate = scrapy.Field()
    publishedAtDate = scrapy.Field()
    hasNewFlag = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    newHomeBuilder = scrapy.Field()
    floorplan = scrapy.Field()
    city = scrapy.Field()
    zip_code = scrapy.Field()
    district = scrapy.Field()
    contact_name = scrapy.Field()
    media_count = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    livingSpace = scrapy.Field()
    rent = scrapy.Field()
    rooms = scrapy.Field()
    extra_costs = scrapy.Field()
    kitchen = scrapy.Field()
    balcony = scrapy.Field()
    garden = scrapy.Field()
    private = scrapy.Field()
    plotArea = scrapy.Field()
    cellar = scrapy.Field()
    time_dest = scrapy.Field()  # time to destination using transit or driving
    time_dest2 = scrapy.Field()
    time_dest3 = scrapy.Field()
    pictureCount = scrapy.Field()
    priceTrend = scrapy.Field()
    rented = scrapy.Field()
    yearConstructed = scrapy.Field()
    condition = scrapy.Field()
    interiorQuality = scrapy.Field()
    numberOfFloors = scrapy.Field()
    buildingType = scrapy.Field()
    heatingType = scrapy.Field()
    heatingFiringType = scrapy.Field()
    energyEfficiencyClass = scrapy.Field()
    parkSpaces = scrapy.Field()
    telekomDownloadSpeed = scrapy.Field()
    telekomUploadSpeed = scrapy.Field()
    telekomTechnology = scrapy.Field()
    telekomInternetType = scrapy.Field()

