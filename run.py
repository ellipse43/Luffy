# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from Luffy.spiders.a52pk import A52pkSpider
from Luffy.spiders.wallbase import WallbaseSpider

process = CrawlerProcess()
process.crawl(A52pkSpider)
process.crawl(WallbaseSpider)
process.start()


