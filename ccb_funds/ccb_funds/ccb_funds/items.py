# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CcbFundsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class SpdbFundsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class CiticbankFundsItem(scrapy.Item):
    # define the fields for your item here like:
    # pname = scrapy.Field()
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class HxbFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class CebFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class PinganFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class AbcFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class BcmFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class CgbFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class CibFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class BocFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class CmbcFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class IcbcFundsItem(scrapy.Item):
    pid = scrapy.Field()
    pname = scrapy.Field()
    prate = scrapy.Field()
    pfloor = scrapy.Field()
    pperiod = scrapy.Field()

class FindBkItem(scrapy.Item):
    pname = scrapy.Field()
