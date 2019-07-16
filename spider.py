# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fangjia.items import FangjiaItem
import re


class CqfjSpider(CrawlSpider):
    name = 'cqfj'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://cq.fang.anjuke.com/loupan/all/p1/']

    rules = (
        Rule(LinkExtractor(allow=r'https://cq\.fang\.anjuke\.com/loupan/all/p\d'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = FangjiaItem()
        item['name']=response.xpath('//span[@class="items-name"]/text()').extract()
        item['location']=response.xpath('//span[@class="list-map"]/text()').extract()
        #price=response.xpath('//a[@class="favor-pos"]/p[@class="favor-tag around-price"]|(//a[@class="favor-pos"]/p[@class="price-txt"]|//a[@class="favor-pos"]/p[@class="price"])')
        price=response.xpath('//a[@class="favor-pos"]')
        price_2=price.xpath('string(.)').extract()
        for i in range (0,len(price_2)):
            price_2[i]=price_2[i].replace('\t','').replace(' ','').replace('\n','')
        item['price']=price_2
        item['tag']=response.xpath('//i[@class="status-icon onsale"]/text()|//i[@class="status-icon forsale"]/text()|//i[@class="status-icon soldout"]/text()').extract()
        size=response.xpath('//a[@class="huxing"]')
        size_2=size.xpath('string(.)').extract()
        for j in range (0,len(size_2)):
            size_2[j]=size_2[j].replace('\t','').replace(' ','').replace('\n','')
        item['size']=size_2        
        item['url']=response.xpath('//a[@class="lp-name"]/@href').extract()
        yield item
