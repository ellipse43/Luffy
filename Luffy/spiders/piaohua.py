# -*- coding: utf-8 -*-

import os

import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class PiaohuaSpider(CrawlSpider):

    name = 'piaohua'
    allowed_domains = ['www.piaohua.com']
    start_urls = ['http://www.piaohua.com/index.html']

    rules = [Rule(LinkExtractor(tags=('a', 'area', 'link', 'script'), attrs=(
        'href', 'src'), deny_extensions=['index\.php', ]), callback='parse_item', follow=True), ]

    def _is_endswith_suffix(self, v):
        for suffix in ['.html', '.htm', '.css', '.js', '.json', '.xml', '.jpg', '.jpeg', '.png', '.ico', '.gif']:
            if v.endswith(suffix):
                return True
        return False

    def parse_item(self, response):
        v = response.url.split('//', 1)[1].strip('/').split('/')
        if self._is_endswith_suffix(v[-1]):
            url = 'downloads/' + '/'.join(v[:-1])
            if not os.path.isdir(url):
                os.makedirs(url)
            with open(url + '/' + v[-1], 'wb') as f:
                f.write(response.body)
        else:
            pass
