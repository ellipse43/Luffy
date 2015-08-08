# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from ..items import WallbaseItem


class WallbaseSpider(CrawlSpider):
    name = 'wallbase'
    allowed_domains = ['alpha.wallhaven.cc']
    start_urls = [
        'http://alpha.wallhaven.cc/search?q=one+piece&page=%d' % x for x in xrange(1, 5)]

    rules = ()

    def parse(self, response):
        links = response.xpath('//*[@id="thumbs"]/section/ul/li')
        for link in links:
            r = link.css('figure > a::attr(href)').extract()
            if r:
                yield Request(r[0], callback=self.parse_item)

    def parse_item(self, response):
        img = response.css('#wallpaper::attr(src)').extract()
        if img:
            item = WallbaseItem()
            item['image_urls'] = ['http:' + img[0], ]
            return item
