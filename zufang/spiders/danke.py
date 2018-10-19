# -*- coding: utf-8 -*-
import hashlib

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from zufang.items import ZufangItem


class DankeSpider(CrawlSpider):
    name = 'danke'
    allowed_domains = ['dankegongyu.com']
    start_urls = ['https://www.dankegongyu.com/room/gz']
    next_url=LinkExtractor(allow=r"https://www.dankegongyu.com/room/gz?page=\d+")
    request_url=LinkExtractor(allow=r"https://www.dankegongyu.com/room/\d+.html")
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"page")]/a[contains(.,">")]')),
        Rule(request_url, callback='parse_item'),
    )

    def parse_item(self, response):
        item = ZufangItem()
        item['name']= response.xpath('//*[contains(@class,"room-name")]/h1/text()').extract()
        item['url'] = response.url
        item['url_id'] = self.get_md5(response.url)
        item['ifhezu'] = response.xpath('//*[contains(@class,"methodroom-rent")]/text()').extract()
        item['zhuangtai'] = self.remove_kongge(response.xpath('//*[contains(@class,"room-title")]//text()').extract())
        item['money'] = response.xpath('//*[contains(@class,"room-price-num")]/text()')[0].extract()
        item['one_money'] = self.remove_kongge(response.xpath('//*[contains(@class,"room-price-sale")]//text()')[0].extract())

        item['size'] = response.xpath('//*[contains(@class,"room-detail-box")] [1]//label[1]/text()')[0].extract()
        item['number'] = response.xpath('//*[contains(@class,"room-detail-box")] [1]//label[1]/text()')[1].extract()

        item['type'] =  self.remove_kongge( response.xpath('//*[contains(@class,"room-detail-box")] [1]//label[1]/text()')[2].extract())

        item['orientation'] = response.xpath('//*[contains(@class,"room-detail-box")] [2]//label[1]/text()')[1].extract()
        item['floor'] = response.xpath('//*[contains(@class,"room-detail-box")] [2]//label[1]/text()')[0].extract()
        item['location'] = response.xpath('//*[contains(@class,"detail-roombox")]/@title').extract()

        item['subway'] = response.xpath('//*[contains(@class,"room-detail-box")] [2]//label[1]/text()')[6].extract()
        item['deploy'] = self.remove_kongge(response.xpath('//*[contains(@class,"room-info-list")]/table/tr[2]//text()').extract())
        if self.if_roomie(response):
            item['roomie'] = self.get_roomie(response)
        return item

# ('//*[contains(@class,"room-name")]/h1/text()')room_name
# '//*[contains(@class,"room-name")]/em/text()'地铁
#'//*[contains(@class,"room-title")]//text()' z状态
# //*[contains(@class,"methodroom-rent")] /text() 合不合租
# //*[contains(@class,"room-price-num")]/text() 月租

# xpath('//*[contains(@class,"room-price-sale")]//text()')[0] 首月月租
# '//*[contains(@class,"room-detail-box")] [1]//label[1]/text()' [0]建筑面积
# '//*[contains(@class,"room-detail-box")] [1]//label[1]/text()' [1]编号
# '//*[contains(@class,"room-detail-box")] [1]//label[1]/text()' [2]户型
# '//*[contains(@class,"room-detail-box")] [1]//label[1]/text()' [4]付款
# //*[contains(@class,"room-detail-box")] [2]//label[1]/text() [1]朝向

# //*[contains(@class,"room-detail-box")] [2]//label[1]/text() [2]楼层
# '//*[contains(@class,"detail-roombox")]/@title' 位置
# //*[contains(@class,"room-detail-box")] [2]//label[1]/text() [4]地铁
# //*[contains(@class,"room-info-list")]/table/tr[2]//text() 房屋配置

# 室友
# titles = selector.xpath('//*[contains(@class,"room-info-firend")]//*[contains(@class,"room_center")]//tbody/tr[1  ]//text()')
# ss="".join(titles)
# print(ss.replace(' ','').replace('\n',' '))

# //*[contains(@class,"room-info-firend")]//*[contains(@class,"room_center")]//tbody/tr[3]/td/a/@href
    def remove_kongge(self,titles):
        ss = "".join(titles)
        ss = ss.replace(' ', '').replace('\n', ' ')
        return ss
    def if_roomie(self,response):
        hezu = response.xpath('//*[contains(@class,"methodroom-rent")]/text()').extract()[0]
        if hezu:
            return True
        else:
            return False

    def get_roomie(self,response):
        detail=""
        titless = response.xpath('//*[contains(@class,"room-info-firend")]//*[contains(@class,"room_center")]//tbody/tr')
        for i in range(0, len(titless)):
            titles = response.xpath(
                '//*[contains(@class,"room-info-firend")]//*[contains(@class,"room_center")]//tbody/tr[{0}]//text()'.format(
                    str(i + 1))).extract()
            ss = "".join(titles)
            ss = ss.replace(' ', '').replace('\n', ' ')
            print(response.url)
            if '可出租' in ss:
                ww = response.xpath( '//*[contains(@class,"room-info-firend")]//*[contains(@class,"room_center")]//tbody/tr[{0}]/td/a/@href '.format(str(i+1))).extract()
                ss = ss + ww[0]
            detail = detail + ss + '\n'

        return detail

    def get_md5(self,url):
        md5 = hashlib.md5()
        md5.update(url.encode(encoding='utf-8'))
        return md5.hexdigest()
