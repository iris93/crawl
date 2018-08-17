# -*- coding: utf-8 -*-
# 工商银行
import scrapy
import json
import re
from ccb_funds.items import FundsInfoItem
class Cibbank(scrapy.Spider):
    name = "icbc"
    allowed_domains = ["icbc.com"]
    start_urls = ['https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&Area_code=4000&requestChannel=302&pageFlag=']
    def start_requests(self):
        for i in range(0,20):
            yield scrapy.FormRequest(
                url = self.start_urls[0]+str(i),
                method = 'GET',
                callback=self.parse)

    def parse(self, response):
        # print "内部网页"
        # print response.body
        indatas = response.xpath('//div[@class="ebdp-pc4promote-circularcontainer"]')
        # print len(indatas)
        # print len(indatas[0].xpath('./div[@class="ebdp-pc4promote-circularcontainer-content"]/table/tbody/tr/td'))
        for data in indatas:

            item = FundsInfoItem()

            item["pname"] = data.xpath('./div[@class="ebdp-pc4promote-circularcontainer-head"]/span/span/a/text()').extract()[0]
            # print item["pname"]
            item["pid"] =  data.xpath('./div[@class="ebdp-pc4promote-circularcontainer-head"]/span/span/a/@href').extract()[0].split('(')[-1].split(',')[0].strip('\'')
        
            temp = data.xpath('./div[@class="ebdp-pc4promote-circularcontainer-content"]/table/tbody/tr/td')
            
            item["prate"] = temp[0].xpath('./div/div')[1].xpath('./text()').extract()[0]
        
            item["pfloor"] = temp[1].xpath('./div/div')[1].xpath('./b/text()').extract()[0]+temp[1].xpath('./div/div')[1].xpath('./text()').extract()[0]
            try:
                item["pperiod"] = temp[2].xpath('./div/div')[1].xpath('./b/text()').extract()[0]
            except:
                item["pperiod"] = temp[2].xpath('./div/div')[1].xpath('./text()').extract()[0]
            yield item
        
