
import scrapy
from giligiliicon.spiders.parseHelper import *

class giligiliSpider_Main(scrapy.Spider):
    name = "giligiliicon"
    start_urls = [
        "http://www.nh87.cn/find.html"
    ]

    def parse(self, response):
        for item in parseActorsIconListHelper(response):
            yield item

    def handleError(self,failure):
        logger.error("HTTP Error-->%s"%(repr(failure)))