# -*- coding: utf-8 -*-
# 民生银行
import scrapy
import json
import re
from bs4 import BeautifulSoup
from ccb_funds.items import CmbcFundsItem

class Cmbccbank(scrapy.Spider):
    name = "cmbc"
    allowed_domains = ["cmbc.com"]
    start_urls = ['http://www.cmbc.com.cn/channelApp/ajax/Financialpage']

    def start_requests(self):
        for i in range(1,10):
            curpage = i
            yield scrapy.FormRequest(
                url = self.start_urls[0],
                formdata={"request":{"body":{"page":'1',"row":'10'},"header":{"device":{"model":"SM-N7508V","osVersion":"4.3","imei":"352203064891579","isRoot":"1","nfc":"1","brand":"samsung","mac":"B8:5A:73:94:8F:E6","uuid":"45cnqzgwplsduran7ib8fw3aa","osType":"01"},"appId":"1","net":{"ssid":"oa-wlan","netType":"WIFI_oa-wlan","cid":"17129544","lac":"41043","isp":"","ip":"195.214.145.199"},"appVersion":"3.60","transId":"Financialpage","reqSeq":"0"}}},
                method = 'POST',
                callback=self.parse)

    def parse(self, response):
        print "打印response"
        # print response.body
        datas = json.loads(response.body)
        print datas
        item = CmbcFundsItem()
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