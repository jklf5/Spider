# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    offset = 0
    baseURL = 'http://hr.tencent.com/position.php?&start='
    start_urls = [baseURL+str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in node_list:
        	item = TencentItem()
        	item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0]
        	item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0]
        	if len(node.xpath("./td[2]/text()")):
        		item['positionType'] = node.xpath("./td[2]/text()").extract()[0]
        	else:
        		item['positionType'] = ""
        	item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0]
        	item['workLocation'] = node.xpath("./td[4]/text()").extract()[0]
        	item['publichTime'] = node.xpath("./td[5]/text()").extract()[0]

        	yield item

        #if self.offset < 2680:
        #    self.offset += 10
        #    url=self.baseURL + str(self.offset)
        #    yield scrapy.Request(url,callback = self.parse)
        #    
        if len(response.xpath("//a[@id='next' and @ class='noactive']")) == 0:
            url=response.xpath("//a[@id='next']/@href").extract()[0]
            baseURL='http://hr.tencent.com/'
            callbackURL=baseURL+url
            yield scrapy.Request(callbackURL,callback = self.parse)
