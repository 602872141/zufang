# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db=self.client['zufang']
    def process_item(self, item, spider):
        self.db['dake'].update({'url_id':item.get('url_id')},{'$set':item},True)
        return item
