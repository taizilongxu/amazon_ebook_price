#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy.orm import sessionmaker
from models import Books, Info, db_connect, create_table
from OpenSSL import SSL
import os

app = Flask(__name__)
api = Api(app)

# ssl
context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), 'resources/my.com.crt')
key = os.path.join(os.path.dirname(__file__), 'resources/my.com.key')
# cer = '~/resources/my.com.crt'
# key = '~/resources/my.com.key'

# db
engine = db_connect()
create_table(engine)
session = sessionmaker(bind=engine)()


class Price(Resource):
    def get(self, book_id):
        book_info = session.query(Info).filter_by(book_id=book_id).all()
        if book_info:
            price = [i.price for i in book_info]
            return price
        else:
            return {}

api.add_resource(Price, '/<string:book_id>')

if __name__ == '__main__':
    context = (cer, key)
    app.run(debug=True, ssl_context=context)
