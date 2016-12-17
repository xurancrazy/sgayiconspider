# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
from twisted.python.compat import cmp

from giligiliicon.spiders.parseHelper import logger, r


class CustomIconImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['img']
        if image_url and cmp(image_url,'http://www.nh87.cn')!=0:
            return scrapy.Request(image_url)
        else:
            raise DropItem("don't request img")


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            logger.error("Item contains no images,imgurl = %s"%(item['img']))
            raise DropItem("Item contains no images")
        item['img_filepath'] = image_paths[0].split('/')[1]
        return item

class MySQLStoreIconGiliGiliPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            port=3306,
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USERNAME'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    #pipeline默认调用
    def process_item(self, item , spider):
        d = self.dbpool.runInteraction(self.upOrInsert, item)
        d.addErrback(self.handleError, item)
        return d

    #将每行更新或写入数据库中
    def upOrInsert(self, conn, item):
        teacher = item['avActor']
        img_filepath = item['img_filepath']
        print("1",teacher,"2",teacher.encode('utf-8'),"3",type(teacher),"4",type(teacher.encode('utf-8')))
        s = 'select * from teachers where name = \'%s\''%(teacher)
        conn.execute(s)
        ret = conn.fetchone()
        if ret:
            if img_filepath:
                s = 'update teachers set img = \'%s\' where name = \'%s\''%(img_filepath,teacher)
                conn.execute(s)

    def handleError(self,failure, item):
        logger.error("database execute error,teacher = %s"%(item['avActor']))
        logger.error(failure)
