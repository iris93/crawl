# -*- coding: utf-8 -*-
# 浙商银行
import scrapy
import re
from ccb_funds.items import FundsInfoItem


class czbSpider(scrapy.Spider):
    name = 'czb'
    allowed_domains = ['czbank.com']
    start_urls = ['http://www.czbank.com/cn/personal/investment/issue/201608/t20160823_3537.shtml']


    def start_requests(self):
        for i in range(1,10):
            curpage = i
            yield scrapy.FormRequest(
                url = self.start_urls[0],
                method = 'GET',
                callback=self.parse_links)

    def parse(self, response):
        page = response.text
        reg = r'(永乐\d号[^<]*).*(\w\w\d\d\d\d).*(\d\.\d\d%).*起点金额(.*)[\S]上限'.decode('utf-8')
        reg = re.compile(reg)
        finfos = reg.findall(page)
        for data in finfos:
            item = FundsInfoItem()
            item["pid"] = data[1]
            item["pname"] = data[0]
            item["prate"] = data[2]
            item["pperiod"] = u'未找到投资期限'
            item["pfloor"] = data[3]
            yield item

    def parse_links(self,response):
        links = response.xpath('//font/a')
        # print len(links)
        # print links[0]
        base = 'http://www.czbank.com/cn/personal/investment/issue/201608/'
        for link in links:
            self.name = link.xpath('@oldsrc').extract()[0]
            url = base + self.name
            # print url
            yield scrapy.Request(url=url,method = 'GET',callback=self.parse_pdf)

    def parse_pdf(self,response):
        # result=response.xpath('//div[@class="page"]//div[@class="textLayer"]')
        print response.url
        filename = 'pdf/'+response.url.split('/')[-1]
        f = open(filename,'wb')
        f.write(response.body)
        f.close()