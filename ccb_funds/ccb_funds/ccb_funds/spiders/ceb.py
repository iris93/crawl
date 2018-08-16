# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ccb_funds.items import CebFundsItem
class Citicbank(scrapy.Spider):
    name = "ceb"
    allowed_domains = ["cebbank.com"]
    # start_urls = ['http://www.cebbank.com/site/gryw/yglc/lccp49/index.html']
    start_urls = ['http://www.cebbank.com/eportal/ui?moduleId=12073&struts.portlet.action=/app/yglcAction!listProduct.action']

    # def start_requests(self):
    #     for i in range(1,10):
    #         curpage = i
    #         yield scrapy.FormRequest(
    #             url = self.start_urls[0],
    #             formdata={'SFZS':'Y','TZBZMC':'RMB','pageSize':'12','page':'1','qxrUp':'Y'},
    #             method = 'POST',
    #             callback=self.parse)

    def parse(self, response):
        print "打印response"
        datas = response
        print response.body
        # print datas[0].xpath('./div/p/a/text()').extract()[0].encode("utf-8")
        # print datas[0].xpath('normalize-space(./div/div[@class="box_lf"]/p[@class="box_num"]/text())').extract()[0]
        # print datas[0].xpath('./div/ul/li/span[@class="amt"]/text()').extract()[0].encode("utf-8")+'万'
        # print datas[0].xpath('normalize-space(./div/ul/li/span[@class="highlight"]/text())').extract()[0].encode("utf-8")
        item = CebFundsItem()
        item["pid"] = 'test'
        # for data in datas:
        #     item = CebFundsItem()
        #     item.pname='test'
            # # item["pid"] = data.xpath('./li/div/p/a/text()').extract()
            # item["pname"] = data.xpath('./div/p/a/text()').extract()[0]
            # # print item["pname"]
            # item["prate"] = data.xpath('normalize-space(./div/div[@class="box_lf"]/p[@class="box_num"]/text())').extract()[0]
            # item["pperiod"] = data.xpath('normalize-space(./div/ul/li/span[@class="highlight"]/text())').extract()[0]
            # item["pfloor"] = data.xpath('./div/ul/li/span[@class="amt"]/text()').extract()[0]+'0000'
        yield item