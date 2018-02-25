# -*- coding: utf-8 -*-
import scrapy
from ctripSpider.items import CtripspiderItem
from scrapy.http import Request

class CtripTestSpider(scrapy.Spider):
    name = 'ctrip_test'
    allowed_domains = ['http://www.ctrip.com/']
    # start_urls = ['http://http://www.ctrip.com//']

    def start_requests(self):
        useragent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        yield Request('http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=SHA&ACity1=CTU&SearchType=S&DDate1=2018-03-01',headers=useragent)

    def parse(self, response):
        node_list = response.xpath("//tr[@class='J_header_row']")
        for node in node_list:
            ctripItem = CtripspiderItem()
            price = node.xpath("./td[@class='price']/span[@class='J_base_price']/span[@class='base_price02']/text()").extract()

            print(price)
            #ctripItem["price"] = price[0]
            yield ctripItem