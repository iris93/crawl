# -*- coding: utf-8 -*-
# 中信银行
import scrapy
import json
import re
from bs4 import BeautifulSoup
from ccb_funds.items import FundsInfoItem

class Citicbank(scrapy.Spider):
    name = "citicbank"
    allowed_domains = ["citicbank.com"]
    start_urls = ['https://etrade.citicbank.com/portalweb/fd/getFinaList.htm']

    def start_requests(self):
        for i in range(1,10):
            curpage = i
            yield scrapy.FormRequest(
                url = self.start_urls[0],
                formdata={'branchId':'701100','totuseAmt':'02','orderField':'ppo_incomerate','orderType':'desc','currentPage':str(curpage),'pageSize':'200','pwdControlFlag':'0','responseFormat':'JSON','random':'7470'},
                method = 'POST',
                callback=self.parse)

    def parse(self, response):
        print "打印response"
        # print response.body
        datas = json.loads(response.body)['content']['resultList']
        print datas[0]
        for data in datas:
            item = FundsInfoItem()
            item["pid"] = data['prdNo']
            item["pname"] = data['prdName']
            item["prate"] = data['incomerate']
            item["pperiod"] = data['dayDeadLine']
            item["pfloor"] = data['firstAmt']
            yield item