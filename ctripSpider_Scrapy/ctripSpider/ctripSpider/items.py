# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CtripspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    logo = scrapy.Field()
    takeofftime = scrapy.Field()
    center = scrapy.Field()
    arrivetime = scrapy.Field()
    service = scrapy.Field()
    price = scrapy.Field()