# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class FindBkPipeline(object):
    

    def open_spider(self, spider):
    	self.file_name =open("{}_funds.txt".format(spider.name),'a') 

    # def process_item(self, item, spider):
    #     with open(self.file_name,'a') as fp:
    #         fp.write(item['name'].encode("utf8") + '\n')

    def process_item(self, item, spider):
        # 这里是将item先转换成字典，在又字典转换成字符串
        # json.dumps转换时对中文默认使用的ascii编码.想输出真正的中文需要指定 ensure_ascii=False
        # 将最后的item 写入到文件中
        text = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file_name.write(text.encode("utf8"))
        # self.file_name.write(item['name'].encode("utf8") + '\n')
        return item

    def close_spider(self):
        self.file_name.close()