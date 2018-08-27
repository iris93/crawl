# -*- coding: utf-8 -*-
# 中国建设银行
import scrapy
import json
import re
import urllib2
from ccb_funds.items import FundsInfoItem

# class CcbGetnews(scrapy.Spider):
#     name = 'ccbgetnews'
#     allowed_domains = ['ccb.com']
#     start_urls = ['http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp?jsoncallback=jsonpCallback']

#     def start_requests(self):
        # yield scrapy.FormRequest(
        #     url = 'http://finance.ccb.com/cc_webtran/queryFinanceProdDetail.gsp?jsoncallback=jQuery191036942510719116894_1533864732025&params.code=ZHQYAX20180600001',
        #     formdata={'jsoncallback':'jQuery191036942510719116894_1533864732025','params.code':'ZHQYAX20180600001'},
        #     method = 'POST',
        #     callback=self.parse)
    
#     def parse(self, response):
#         print(response.text)


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

    def get_ccb_detail_rate(self, params_code = 'ZHQYAX20180600001'):
        try:
            url = r'http://finance.ccb.com/cc_webtran/queryFinanceProdDetail.gsp?'
            headers = {
                'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                'Referer': r'http://finance.ccb.com/cn/finance/product.html',
                'Connection': 'keep-alive'
            }
            data = {'jsoncallback':'jQuery191036942510719116894_1533864732025','params.code': params_code}
            data = urllib2.parse.urlencode(data).encode('utf-8')
            req = urllib2.request.Request(url, headers=headers, data=data)
            page = urllib2.request.urlopen(req).read()
            page = page.decode('gbk')
            begin = re.search('jQuery191036942510719116894_1533864732025', page).end()
            page = json.loads(page[begin + 1:-1])
            page = page["pubNoticeUrl"]
            news_url = re.findall(r'@@\|.{70,130}\|@#', page)[0][3:-3]
            req2 = urllib2.request.Request(news_url, headers=headers)
            page_detail = urllib2.request.urlopen(req2).read()
            reg_rate = r'>(.{0,5}%)<'
            reg_rate = re.compile(reg_rate)
            last_rate = reg_rate.search(page_detail.decode('utf-8')).group(1)
            return last_rate
        except :
            err_msg = '无法获取到收益率'
            return err_msg


    def parse(self, response):
        begin = re.search('jsonpCallback', response.text).end()
        datas = json.loads(response.text[begin+1:-1])['ProdList']
        for data in datas:
            if data["yieldRate"]==0.0 :
                # 试图从子页面抓取最新收益率
                data["yieldRate"] = self.get_ccb_detail_rate(data['code'])
            item = FundsInfoItem()
            item["pid"] = data['code']
            item["pname"] = data['name']
            item["prate"] = data['yieldRate']
            item["pperiod"] = data['investPeriod']
            item["pfloor"] = data['purFloorAmt']
            # item["pscale"] = data['instructionUrl']
            yield item
