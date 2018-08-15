# -*- coding: utf-8 -*-
import scrapy
from find_bk.items import FindBkItem
 
class MeijuSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["meijutt.com"]
    start_urls = ['http://www.meijutt.com/new100.html']
 
    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_movie in movies:
            item = FindBkItem()
            print each_movie
            item['name'] = each_movie.xpath('./h5/a/@title').extract()[0]
            yield item