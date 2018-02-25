# -*- coding: utf-8 -*-
import scrapy
from ScrapySpider.items import ScrapyspiderItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['www.itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        node_list=response.xpath("//div[@class='li_txt']")
        #用来存储所有items字段
        for node in node_list:
            #创建items对象，用来存储信息
            item=ScrapyspiderItem()
            name=node.xpath("./h3/text()").extract()
            title=node.xpath("./h4/text()").extract()
            info=node.xpath("./p/text()").extract()

            item['name']=name[0]
            item['title']=title[0]
            item['info']=info[0]

            yield item

