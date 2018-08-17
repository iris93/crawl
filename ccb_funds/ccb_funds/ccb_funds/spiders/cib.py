# -*- coding: utf-8 -*-
# 兴业银行
import scrapy
import json
import re
from ccb_funds.items import CibFundsItem
class Cibbank(scrapy.Spider):
    name = "cib"
    allowed_domains = ["cib.com"]
    start_urls = ['http://wealth.cib.com.cn/retail/onsale/index.html']
    def start_requests(self):
        yield scrapy.FormRequest(
            url = self.start_urls[0],
            method = 'GET',
            callback=self.parse)

    def parse(self, response):
        print "内部网页"
        # print response.body
        indatas = response.xpath('//tbody/tr')
        print len(indatas)
        
        for data in indatas:
            item = CibFundsItem()
            try :
                item["pname"] = data.xpath('./td')[0].xpath('./a/text()').extract()[0]
            except:
                item["pname"] = data.xpath('./td')[0].xpath('./text()').extract()[0]
            item["pid"] = data.xpath('./td')[-1].xpath('./img/@src').extract()[0].split('lccp')[-1].split('.')[0]

            item["prate"] = data.xpath('./td')[6].xpath('./text()').extract()[0]
        
            item["pfloor"] = data.xpath('./td')[5].xpath('./text()').extract()[0]
        
            item["pperiod"] = data.xpath('./td')[4].xpath('./text()').extract()[0]
            yield item
        
