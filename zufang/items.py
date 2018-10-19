# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # define the fields for your item here like:
    # 名字
    name = scrapy.Field()
    # 链接
    url = scrapy.Field()
    # 链接id
    url_id =scrapy.Field()
    # 是否支持合租
    ifhezu = scrapy.Field()
    # 房子状态
    zhuangtai = scrapy.Field()
    # 月租
    money = scrapy.Field()
    # 首月月租
    one_money = scrapy.Field()
    # 面积
    size = scrapy.Field()
    # 编号
    number = scrapy.Field()
    # 户型
    type = scrapy.Field()
     # 朝向
    orientation = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 位置
    location = scrapy.Field()
    # 地铁
    subway = scrapy.Field()
    # 房屋配置
    deploy = scrapy.Field()
    # 室友以及其它位置情况
    roomie = scrapy.Field()


# '//*[contains(@class,"room-detail-box")] [1]//label[1]/text()' [2]户型
# '//*[contains(@class,"room-detail-box")] [1]//label[1]/text()' [4]付款
# //*[contains(@class,"room-detail-box")] [2]//label[1]/text() [1]朝向
# //*[contains(@class,"room-detail-box")] [2]//label[1]/text() [2]楼层
# '//*[contains(@class,"detail-roombox")]/@title'区域
# //*[contains(@class,"room-detail-box")] [2]//label[1]/text() [4]地铁
# //*[contains(@class,"room-info-list")]/table/tr[2]//text() 房屋配置