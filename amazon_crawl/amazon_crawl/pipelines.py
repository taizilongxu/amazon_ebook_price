# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Books, Info, db_connect, create_table
from scrapy.exceptions import DropItem
from datetime import datetime, timedelta


class AmazonCrawlPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        book = Books(book_id=item['book_id'],
                     tag=item['tag'],
                     name=item['name'],
                     author=item['author'],
                     public_date=item['public_date'])
        info = Info(book_id=item['book_id'],
                    price=item['price'],
                    comment_num=item['comment_num'],
                    star=item['star'])

        if not session.query(Info).filter(book_id=item['book_id']).filter(cast(Info.create_date,Date) == datetime.date.today()).fisrt():
            session.add(info)
            session.commit()
        try:
            if not session.query(Books).filter_by(book_id=item['book_id']).first():
                session.add(book)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['book_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['book_id'])
            return item