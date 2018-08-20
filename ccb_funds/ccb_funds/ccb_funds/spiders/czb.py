# -*- coding: utf-8 -*-
# 浙商银行
import scrapy
import re
from ccb_funds.items import FundsInfoItem


class czbSpider(scrapy.Spider):
    name = 'czb'
    allowed_domains = ['czbank.com']
    start_urls = ['http://www.czbank.com/cn/personal/investment/issue/201608/t20160823_3537.shtml']


    def parse(self, response):
        page = response.text
        reg = r'(永乐\d号[^<]*).*(\w\w\d\d\d\d).*(\d\.\d\d%).*起点金额(.*)[\S]上限'
        reg = re.compile(reg)
        finfos = reg.findall(page)
        for data in finfos:
            item = FundsInfoItem()
            item["pid"] = data[1]
            item["pname"] = data[0]
            item["prate"] = data[2]
            item["pperiod"] = u'未找到投资期限'
            item["pfloor"] = data[3]
            yield item
