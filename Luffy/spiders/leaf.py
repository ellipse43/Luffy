# -*- coding: utf-8 -*-

import os
import urlparse
import traceback
import requests
from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from ..items import LeafItem
from ..utils import leaf


class LeafSpider(scrapy.Spider):

    name = 'leaf'
    allowed_domains = ['gitbook.com', 'gitbooks.io']
    start_urls = ['https://www.gitbook.com/explore?page=%d' %
                  x for x in range(0, 1)]

    def parse(self, response):
        # fix
        d = response.css(
            '#page-explore-homepage > div.gb-page-inner > div > div.books-list > div > div > div > div.book-inner > div.book-infos > h3 > a::attr(href)')
        for x in d:
            uri = 'https://www.gitbook.com' + x.extract()
            yield Request(uri, callback=self.leaf)

    def leaf(self, response):

        def _extract(css):
            try:
                return response.css(css)[0].extract().strip()
            except:
                traceback.print_exc()
            return None

        configs = {
            'name': '#page-book-details > div.book-header > div > div > div.col-md-9 > div.details-intro > div > h1::text',
            'pic_uri': '#page-book-details > div.book-header > div > div > div.col-md-3 > div > img::attr(src)',
            'description': '#page-book-details > div.book-header > div > div > div.col-md-9 > div.details-intro > div > p.book-description::text',
            'author': '#page-book-details > div.book-header > div > div > div.col-md-9 > div.details-intro > div > p.book-authors > a:nth-child(2)::text',
            'author_uri': '#page-book-details > div.book-header > div > div > div.col-md-9 > div.details-intro > div > p.book-authors > a:nth-child(2)::attr(href)'
        }

        item = LeafItem()

        uri = _extract(
            '#page-book-details > div.book-header > div > div > div.col-md-9 > div.details-intro > div > div > div:nth-child(1) > a::attr(href)')

        if uri:
            item['uri'] = 'https://www.gitbook.com' + uri
            item['created_date'] = datetime.now()
            item['updated_date'] = datetime.now()

            for key, value in configs.items():
                item[key] = _extract(value)

            try:
                res = requests.get(item['uri'])
                item['path'] = res.url
                return item
            except:
                print item['uri']
                traceback.print_exc()


class DownloadSpider(CrawlSpider):

    name = 'download'
    allowed_domains = list(
        set([urlparse.urlsplit(url).netloc for url in leaf()]))
    start_urls = leaf()

    rules = [Rule(LinkExtractor(tags=('a', 'area', 'link', 'script'), attrs=(
        'href', 'src'), deny_extensions=''), callback='parse_item'), ]

    def parse_item(self, response):
        # url_path = 'downloads/gitbooks/' + \
        #     urlparse.urlsplit(response.url).path.strip('/').lstrip('-')
        url_path = 'downloads/gitbooks/' + response.url.split('//', 1)[1].strip('/')
        if not os.path.isdir(url_path.rsplit('/', 1)[0]):
            os.makedirs(url_path.rsplit('/', 1)[0])
        with open(url_path, 'wb') as f:
            f.write(response.body)
