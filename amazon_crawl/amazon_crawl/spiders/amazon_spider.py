#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from amazon_crawl.items import AmazonCrawlItem

class DmozSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.cn"]
    start_urls = [
        "https://www.amazon.cn/Kindle%E7%94%B5%E5%AD%90%E4%B9%A6/b/ref=sa_menu_kindle_l2_116169071?ie=UTF8&node=116169071",
    ]

    def parse(self, response):
        req = []
        cate_name = response.xpath('//*[@id="ref_116169071"]/li/a/span[1]/text()').extract()
        cate_num = response.xpath('//*[@id="ref_116169071"]/li/a/span[2]/text()').extract()[1:]
        cate_url = response.xpath('//*[@id="ref_116169071"]/li/a/@href').extract()[1:]
        for index, i in enumerate(cate_name):
            print i, cate_num[index], cate_url[index]
            r = Request(cate_url[index], callback=self.parse_cate)
            req.append(r)
        return req

    def parse_cate(self, response):
        req = []
        cate_child_name = response.xpath('//div[@class="categoryRefinementsSection"]/ul[1]/li/a/span[1]/text()').extract()
        cate_child_num = response.xpath('//div[@class="categoryRefinementsSection"]/ul[1]/li/a/span[2]/text()').extract()[2:]
        cate_child_url = response.xpath('//div[@class="categoryRefinementsSection"]/ul[1]/li/a/@href').extract()[2:]
        for index, i in enumerate(cate_child_name):
            print i, cate_child_num[index], cate_child_url[index]
            r = Request(cate_child_url[index], callback=self.parse_list)
            req.append(r)
        return req

    def parse_list(self, response):
        req = []
        products_name = response.xpath('//li[@class="s-result-item celwidget"]//h2/text()').extract()
        products_price = response.xpath('//span[@class="a-size-base a-color-price s-price a-text-bold"]/text()').extract()
        products_author = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[2]/div/span[2]/text()').extract()
        products_public_date = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[2]/span[3]/text()').extract()
        products_comment_num = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[3]/div[2]/div/a/text()').extract()
        products_stars = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[3]/div[2]/div/span/span/a/i[1]/span/text()').extract()
        products_book_ids = response.xpath('//li[@class="s-result-item celwidget"]/@data-asin').extract()

        # rule the data
        products_price = [float(i[1:]) for i in products_price]
        products_comment_num = [int(''.join(i.split(','))) for i in products_comment_num]
        products_stars = [float(i.split(' ')[0][2:]) for i in products_stars]


        for name, price, author, public_date, comment_num, star, book_id in zip(products_name, products_price, products_author, products_public_date, products_comment_num, products_stars, products_book_ids):
            print book_id, name, price, author, public_date, comment_num, star
            # save item
            item = AmazonCrawlItem()
            item['name'] = name
            item['price'] = price
            item['author']= author
            item['public_date'] = public_date
            item['comment_num'] = comment_num
            item['star'] = star
            item['book_id'] = book_id
            yield item

        next_page = response.xpath('//*[@id="pagnNextLink"]/@href').extract()
        if next_page:
            yield Request('https://www.amazon.cn' + next_page[0], callback=self.parse_list)

