# -*- coding: utf-8 -*-
# 农业银行
import scrapy
import json
import re
from ccb_funds.items import FundsInfoItem
class Pinganbank(scrapy.Spider):
    name = "abc"
    allowed_domains = ["abchina.com"]
    start_urls = ['http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?s=20&o=0&w=%25E5%258F%25AF%25E5%2594%25AE%257C%257C%257C%257C%257C%257C%257C1%257C%257C0%257C%257C0&i=',\
    'http://ewealth.abchina.com/fs']
    def start_requests(self):
        for i in range(1,2):
            yield scrapy.FormRequest(
                url = self.start_urls[0]+str(i),
                method = 'GET',
                callback=self.parse)

    def parse(self, response):
        # print "打印response"
        datas=response.xpath('//Table')
        # print len(datas)
        for data in datas[0:1]:
            item = FundsInfoItem()
            item["pid"] = data.xpath('./ProductNo/text()').extract()[0]
            item["pname"] = data.xpath('./ProdName/text()').extract()[0]
            item["prate"] = data.xpath('./ProdProfit/text()').extract()[0]
            item["pperiod"] = data.xpath('./ProdLimit/text()').extract()[0]
            item["pfloor"] = data.xpath('./PurStarAmo/text()').extract()[0]
            productUrl = self.start_urls[1]+'/'+str(item["pid"])+'.htm'
            # print productUrl
            # productUrl = 'http://ewealth.abchina.com/fs/ADRY180122B.htm'
            yield scrapy.FormRequest(url=productUrl,method='GET',meta={"item":item},callback=self.parse_pdf)
    
    def parse_pdf(self,response):
        # print response
        item = response.meta['item']
        print item
        print "产品详情"
        subUrl = response.xpath('//tr/td/a/@href').extract()[0].strip('.')
        pdfUrl= self.start_urls[1]+subUrl
        print pdfUrl
        yield scrapy.FormRequest(url=pdfUrl,method='GET',meta={"item":item},callback=self.get_scale)

    def get_scale(self,response):
        item = response.meta['item']
        filename = 'pdf/'+response.url.split('/')[-1]
        f = open(filename,'wb')
        f.write(response.body)
        f.close()