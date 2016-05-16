# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    author = scrapy.Field()
    public_date = scrapy.Field()
    comment_num = scrapy.Field()
    star = scrapy.Field()
    book_id = scrapy.Field()
    create_date = scrapy.Field()
