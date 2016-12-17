# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IconItem(scrapy.Item):
    avActor = scrapy.Field()
    img = scrapy.Field() #nh87's img url
    img_result = scrapy.Field() #save request result for nh87's img url
    img_filepath = scrapy.Field() #native's img url
