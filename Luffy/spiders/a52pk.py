# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request

from ..items import OpArticleItem


class A52pkSpider(scrapy.Spider):
    name = "52pk"
    allowed_domains = ["op.52pk.com"]
    start_urls = (
        'http://op.52pk.com/shtml/fenxi.shtml',
    )

    def parse(self, response):
        lis = response.css(
            '#main > div.content.mt10 > div.listbox.cc > ul.list > li > a::attr(href)')
        for li in lis:
            yield Request(li.extract(), callback=self.parse_item)

        next = response.css(
            '#main > div.content.mt10 > div.listbox.cc > div.page > a:nth-child(3)::attr(href)')[0]
        if next:
            yield Request(next.extract(), callback=self.parse)

    def parse_item(self, response):
        article = None
        if not response.meta.get('article'):
            name = response.css(
                '#main > div.content.mt10 > div.show.listbox > div:nth-child(1) > h2::text')[0].extract()
            intro = response.css(
                '#main > div.content.mt10 > div.show.listbox > div.msg > div.m_left::text')[0].extract()
            content = response.css('#article')[0].extract()
            if name and intro and content:
                article = OpArticleItem()
                article['name'] = name
                article['intro'] = intro
                article['content'] = content
        else:
            content = response.css('#article')[0].extract()
            article = response.meta['article']
            article['content'] += content

        next = response.css('#center > a:nth-child(3)::attr(href)')
        if next and article:
            try:
                yield Request(next[0].extract(), callback=self.parse_item, meta={'article': article})
            except:
                if article:
                    yield article
        elif article:
            yield article
