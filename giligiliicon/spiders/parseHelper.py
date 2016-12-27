# -*- coding: utf-8 -*-
import logging

import redis

from giligiliicon.items import IconItem

handler = logging.FileHandler('log/giligili.log')  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('giligili')  # 获取名为giligili的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.INFO)
r =redis.StrictRedis(host='localhost',password='giligilisgay',port=6379)

def parseActorsIconListHelper(response):
    allActor = response.xpath('//*[@id="all"]/div')
    for actor in allActor:
        try:
            item = IconItem()
            hrefUrl = actor.xpath('a/img/@data-original').extract()[0]
            avactor = actor.xpath('div[2]/h2/text()').extract()[0]
            print('avactor = ',avactor,'href = ',hrefUrl)
            item['avActor'] = avactor
            item['img'] = hrefUrl
            if r.sismember("url:crawled:teacher",avactor):
                continue
            yield item
        except Exception as e:
            logger.error("Exception-->parseActorsIconListHelper:%s ,url = %s" % (e, hrefUrl))
