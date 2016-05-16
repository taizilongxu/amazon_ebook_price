#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import Selector

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
            break
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
            break
        return req

    def parse_list(self, response):
        req = []
        products_name = response.xpath('//li[@class="s-result-item celwidget"]//h2/text()').extract()
        products_price = response.xpath('//span[@class="a-size-base a-color-price s-price a-text-bold"]/text()').extract()
        products_author = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[2]/div/span[2]/text()').extract()
        products_data = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[2]/span[3]/text()').extract()
        for name, price, author, data in zip(products_name, products_price, products_author, products_data):
            print name, price, author, data
        next_page = response.xpath('//*[@id="pagnNextLink"]/@href').extract()
        if next_page:
            return [Request('https://www.amazon.cn' + next_page[0], callback=self.parse_list)]
