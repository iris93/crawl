# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ccb_funds.items import SpdbFundsItem


class SpdbSpider(scrapy.Spider):
    name = 'spdb'
    allowed_domains = ['spdb.com.cn']
    start_urls = ['http://per.spdb.com.cn/was5/web/search']
    
    def start_requests(self):
        for i in range(1,10):
            curpage = i
            yield scrapy.FormRequest(
                url = self.start_urls[0],
                formdata={'channelid':'266906','metadata':'finance_state|finance_no|finance_allname|finance_anticipate_rate|finance_limittime|finance_lmttime_info|finance_type|docpuburl|finance_ipo_enddate|finance_indi_ipominamnt|finance_indi_applminamnt|finance_risklevel|product_attr|finance_ipoapp_flag|finance_next_openday',\
                'searchword':'(product_type=3)*finance_limittime = %*(finance_currency = 01)*(finance_state=\'可购买\')','page':str(curpage)},
                method = 'POST',
                callback=self.parse)

    def parse(self, response):
        datas = json.loads(response.text)['rows']
        print(datas[1])
        for data in datas:
            item = SpdbFundsItem()
            item["pid"] = data['finance_no']
            item["pname"] = data['finance_allname']
            item["prate"] = data['finance_anticipate_rate']
            item["pperiod"] = data['finance_lmttime_info']
            item["pfloor"] = data['finance_indi_ipominamnt']
            yield item
