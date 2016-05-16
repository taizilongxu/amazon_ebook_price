# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Books, Info, db_connect, create_table

class AmazonCrawlPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        book = Books(book_id=item['book_id'],
                     name=item['name'],
                     author=item['author'],
                     public_date=item['public_date'])
        info = Info(book_id=item['book_id'],
                    price=item['price'],
                    comment_num=item['comment_num'],
                    star=item['star'])

        try:
            session.add(book)
            session.add(info)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
