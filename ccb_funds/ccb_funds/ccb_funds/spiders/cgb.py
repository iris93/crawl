# -*- coding: utf-8 -*-
# 广发银行
import scrapy
import json
import re
from ccb_funds.items import CgbFundsItem
class Cgbbank(scrapy.Spider):
    name = "cgb"
    allowed_domains = ["cgbchina.com"]
    start_urls = ['http://www.cgbchina.com.cn/Channel/16684283?nav=2']
    def start_requests(self):
        yield scrapy.FormRequest(
            url = self.start_urls[0],
            method = 'GET',
            callback=self.parse)

    def parse(self, response):
        # print "内部网页"
        # print response.body
        indatas = response.xpath('//tr[@class="bg2"]')
        # print len(indatas)
        # item = CgbFundsItem()
        # item["pid"] = "test"
        for data in indatas:
            item = CgbFundsItem()
            item["pname"] = data.xpath('normalize-space(./td[@class="name"]/a/text())').extract()[0]
        
            item["pid"] = data.xpath('./td[@class="name"]/a/@href').extract()[0].split('productno=')[-1]

            item["prate"] = data.xpath('./td')[4].xpath('./b/text()').extract()[0]
        
            item["pfloor"] = data.xpath('./td')[3].xpath('./text()').extract()[0]
        
            item["pperiod"] = data.xpath('./td')[2].xpath('./text()').extract()[0]
            yield item
        
