import scrapy

class FangjiaItem(scrapy.Item):
    name=scrapy.Field()
    location=scrapy.Field()
    price=scrapy.Field()
    tag=scrapy.Field()
    size=scrapy.Field()
    url=scrapy.Field()
