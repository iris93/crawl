# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FindBkItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class CiticbankFundsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()