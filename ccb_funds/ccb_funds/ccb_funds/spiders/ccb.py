# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ccb_funds.items import CcbFundsItem


class CcbSpider(scrapy.Spider):
    name = 'ccb'
    allowed_domains = ['ccb.com']
    start_urls = ['http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp?jsoncallback=jsonpCallback']
    
    def start_requests(self):
        yield scrapy.FormRequest(
            url = self.start_urls[0],
            formdata={'pageNo':'1','pageSize':'100000','queryForm.brand':'03','queryForm.saleStatus':'-1'},
            method = 'POST',
            callback=self.parse)

    def news_requests(self):
        yield scrapy.FormRequest(
            url = self.start_urls[0],
            formdata={'pageNo':'1','pageSize':'100000','queryForm.brand':'03','queryForm.saleStatus':'-1'},
            method = 'POST',
            callback=self.parse)

    def parse(self, response):
    	print("begin")
    	begin = re.search('jsonpCallback', response.text).end()
    	filename = 'ccb.txt'
    	datas = json.loads(response.text[begin+1:-1])['ProdList']
    	for data in datas:
            item = CcbFundsItem()
            item["pid"] = data['code']
            item["pname"] = data['name']
            item["prate"] = data['yieldRate']
            item["pperiod"] = data['investPeriod']
            item["pfloor"] = data['purFloorAmt']
            yield item
