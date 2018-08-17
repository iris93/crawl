# -*- coding: utf-8 -*-
import scrapy
from ccb_funds.items import FundsInfoItem
 
class MeijuSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["meijutt.com"]
    start_urls = ['http://www.meijutt.com/new100.html']
 
    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        print "打印response"
        print movies
        for each_movie in movies:
            item = FundsInfoItem()
            # print each_movie
            # item['name'] = each_movie.xpath('./h5/a/@title').extract()[0]
            item['name'] = 'test'
            yield item