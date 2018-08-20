# -*- coding: utf-8 -*-
# 光大银行
import scrapy
import json
import re
from ccb_funds.items import FundsInfoItem

class Cebcbank(scrapy.Spider):
    name = "ceb"
    allowed_domains = ["cebbank.com"]
    start_urls = ['http://www.cebbank.com/eportal/ui?moduleId=12073&struts.portlet.action=/app/yglcAction!listProduct.action']


    def start_requests(self):
        for i in range(1,20):
            curpage = i
            yield scrapy.FormRequest(
                url = self.start_urls[0],
                formdata={
            'channelIds[]': ['yxl94','ygelc79','hqb30','dhb2','cjh','gylc70','Ajh67','Ajh84','901776','Bjh91',
                        'Ejh99','Tjh70','tcjh96','ts43','ygjylhzhMOM25','yxyg87','zcpzjh64','wjyh1','smjjb9',
                        'ty90','tx16','ghjx6','wf36','ygxgt59','wbtcjh3','wbBjh77','wbTjh28','sycfxl','cfTjh',
                        'jgdhb','tydhb','jgxck','jgyxl','tyyxl','dgBTAcp','27637097','27637101','27637105',
                        '27637109','27637113','27637117','27637121','27637125','27637129','27637133',
                        'gyxj32','yghxl','ygcxl','ygjxl','ygbxl','ygqxl','yglxl','ygzxl'],
            'codeOrName': '',
            'TZBZMC': '',
            'QGJE': '',
            'QGJELEFT': '',
            'QGJERIGHT': '',
            'CATEGORY': '',
            'CPQXLEFT': '',
            'CPQXRIGHT': '',
            'CPFXDJ': '',
            'SFZS': 'Y',
            'qxrUp': 'Y',
            'qxrDown': '',
            'dqrUp': '',
            'dqrDown': '',
            'qdjeUp': '',
            'qdjeDown': '',
            'qxUp': '',
            'qxDown': '',
            'yqnhsylUp': '',
            'yqnhsylDown': '',
            'page': str(i),
            "pageSize": "5"
},
                method = 'POST',
                callback=self.parse)

    def parse(self, response):
        # print "打印response"
        # print len(response.xpath('//div[@class="lccp_main_content_tx"]/ul/li'))
        # datas = response.xpath('//div[@class="lccp_main_content_tx"]/ul/li')
        datas = response.xpath('//div[@class="lccp_main_content_lb"]/table/tbody/tr')
        # print len(datas)
        for data in datas[1:]:
            item = FundsInfoItem()
            temp = data.xpath('./td')
            # print len(temp)
            item["pid"] = temp[0].xpath('./a/@data-analytics-click').extract()[0].split('-')[-1]
            item["pname"] = temp[0].xpath('normalize-space(./a/text())').extract()[0]
            item["prate"] = temp[5].xpath('normalize-space(./div/span/text())').extract()[0]
            item["pperiod"] =temp[4].xpath('normalize-space(./text())').extract()[0]
            item["pfloor"] = temp[3].xpath('normalize-space(./text())').extract()[0]
            yield item