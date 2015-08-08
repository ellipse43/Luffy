# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LuffyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class OpArticleItem(scrapy.Item):
    name = scrapy.Field()
    intro = scrapy.Field()
    content = scrapy.Field()


class WallbaseItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class LeafItem(scrapy.Item):

    name = scrapy.Field()
    pic_uri = scrapy.Field()
    description = scrapy.Field()

    uri = scrapy.Field()
    path = scrapy.Field()

    created_date = scrapy.Field()
    updated_date = scrapy.Field()

    author = scrapy.Field()
    author_uri = scrapy.Field()

