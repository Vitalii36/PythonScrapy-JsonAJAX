# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os
from ScrapyAJAX.items import ScrapyajaxItem

Base = declarative_base()

class SCATable(Base):
    __tablename__ = 'SCAdata'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    author = Column(String)
    tags = Column(String)

    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

    @property
    def __repr__(self):
        return "<Data %s, %s, %s>" % (self.text, self.author, self.tags)


class ScrapyajaxPipeline(object):
    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)

    def process_item(self, item, spider):
        if isinstance(item, ScrapyajaxItem):
            dt = SCATable(item['text'],item['author'], item['tags'])
            self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)
