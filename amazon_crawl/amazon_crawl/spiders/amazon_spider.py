#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from amazon_crawl.items import AmazonCrawlItem

class DmozSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.cn"]
    start_urls = [
    "https://www.amazon.cn/Kindle%E7%94%B5%E5%AD%90%E4%B9%A6/b/ref=sa_menu_kindle_l2_116169071?ie=UTF8&node=116169071"
        # "https://www.amazon.cn/s/ref=lp_116087071_il_to_digital-text?rh=n%3A116087071&ie=UTF8&qid=1463511272&lo=none"
    ]

    def parse(self, response):
        req = []
        cate_name = response.xpath('//*[@id="ref_116169071"]/li/a/span[1]/text()').extract()
        cate_num = response.xpath('//*[@id="ref_116169071"]/li/a/span[2]/text()').extract()[1:]
        cate_url = response.xpath('//*[@id="ref_116169071"]/li/a/@href').extract()[1:]
        for index, i in enumerate(cate_name):
            print i, cate_num[index], cate_url[index]
            r = Request('https://www.amazon.cn' + cate_url[index], callback=self.parse_cate)
            req.append(r)
        return req

    def parse_cate(self, response):
        req = []
        cate_child_name = response.xpath('//div[@class="categoryRefinementsSection"]/ul[1]/li/a/span[1]/text()').extract()
        cate_child_num = response.xpath('//div[@class="categoryRefinementsSection"]/ul[1]/li/a/span[2]/text()').extract()[2:]
        cate_child_url = response.xpath('//div[@class="categoryRefinementsSection"]/ul[1]/li/a/@href').extract()[2:]
        for index, i in enumerate(cate_child_name):
            print i, cate_child_num[index], cate_child_url[index]
            r = Request('https://www.amazon.cn' + cate_child_url[index], callback=self.parse_cate_price)
            req.append(r)
        return req

    def parse_cate_price(self, response):
        req = []
        urls = response.xpath('//*[@id="ref_149573071"]/li/a/@href').extract()
        for url in urls:
            r = Request('https://www.amazon.cn' + url, callback=self.parse_list)
            req.append(r)
        return req

    # def parse_16_to_60(self, response):
    #     rh = response.xpath('//*[@id="s-result-info-bar-content"]/div[2]/div/div/span[2]/a/@href').extract()[0].split('&')[2]
    #     url = 'https://www.amazon.cn/s/ref=sr_il_ti_digital-text?' + rh + '&ie=UTF8&qid=1463537591&lo=digital-text'
    #     yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        req = []
        products_name = response.xpath('//li[@class="s-result-item celwidget"]//h2/text()').extract()
        products_tags = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[3]/div[1]/div[1]/a/h3/text()').extract()
        products_price = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[3]/div[1]/div[last()-1]/a/span[1]/text()').extract()
        products_author = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[2]/div/span[2]/text()').extract()
        products_public_date = response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[2]/span[3]/text()').extract()

        products_comment_num = []
        for i in response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[3]/div[2]'):
            tmp = i.xpath('div/a/text()').extract()
            if tmp:
                products_comment_num.append(int(''.join(tmp[0].split(','))))
            else:
                products_comment_num.append(0)
        products_stars = []
        for i in response.xpath('//li[@class="s-result-item celwidget"]/div/div/div/div[2]/div[3]/div[2]'):
            tmp = i.xpath('div/span/span/a/i[1]/span/text()').extract()
            if tmp:
                products_stars.append(tmp[0])
            else:
                products_stars.append(u'平均0 分')
        products_book_ids = response.xpath('//li[@class="s-result-item celwidget"]/@data-asin').extract()

        # rule the data
        products_price = [float(''.join(i[1:].split(','))) for i in products_price]
        products_stars = [float(i.split(' ')[0][2:]) for i in products_stars]

        for name, tag, price, author, public_date, comment_num, star, book_id in zip(products_name, products_tags, products_price, products_author, products_public_date, products_comment_num, products_stars, products_book_ids):
            print book_id, tag, name, price, author, public_date, comment_num, star
            # save item
            item = AmazonCrawlItem()
            item['tag'] = tag
            item['name'] = name
            item['price'] = price
            item['author'] = author
            item['public_date'] = public_date
            item['comment_num'] = comment_num
            item['star'] = star
            item['book_id'] = book_id
            yield item

        next_page = response.xpath('//*[@id="pagnNextLink"]/@href').extract()
        if next_page:
            yield Request('https://www.amazon.cn' + next_page[0], callback=self.parse_list)

