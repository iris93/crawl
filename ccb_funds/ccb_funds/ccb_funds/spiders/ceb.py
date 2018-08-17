# -*- coding: utf-8 -*-
# 中信银行
import scrapy
import json
import re
from bs4 import BeautifulSoup
from ccb_funds.items import CebFundsItem

class Cebcbank(scrapy.Spider):
    name = "ceb"
    allowed_domains = ["cebbank.com"]
    start_urls = ['http://www.cebbank.com/eportal/ui?moduleId=12073&struts.portlet.action=/app/yglcAction!listProduct.action']

    def start_requests(self):
        for i in range(1,10):
            curpage = i
            yield scrapy.FormRequest(
                url = self.start_urls[0],
                formdata={},
                method = 'POST',
                callback=self.parse)

    def parse(self, response):
        print "打印response"
        print response.body
        datas = json.loads(response.body)
        print datas
        item = CebFundsItem()
        item["pid"] = "test"
        yield item
        # for data in datas:
        #     item = CmbcFundsItem()
        #     item["pid"] = data['prdNo']
        #     item["pname"] = data['prdName']
        #     item["prate"] = data['incomerate']
        #     item["pperiod"] = data['dayDeadLine']
        #     item["pfloor"] = data['firstAmt']
        #     yield item