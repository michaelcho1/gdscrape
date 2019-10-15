# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TsrItem(scrapy.Item):
    tsr_one_ytd_return = scrapy.Field()
    ticker = scrapy.Field()
    begyear = scrapy.Field()
    endyear = scrapy.Field()
    beg = scrapy.Field()
    end = scrapy.Field()


