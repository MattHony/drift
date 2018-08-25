# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/30 20:44
# @Author : '红文'
# @File : gift.py
# @Software: PyCharm
from collections import namedtuple

from flask import current_app
from sqlalchemy.orm import relationship

from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func

from app.spider.yushu_book import YuShuBook


# EachGiftWishCount = namedtuple('EacGiftWishCount', ['count', 'isbn'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish

        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        # count_list = [EachGiftWishCount(w[0], w[1]) for w in count_list]
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 复杂的SQL语句编写
    # 实例方法 转换成 类方法 静态方法
    @classmethod
    def recent(cls):
        # 链式调用
        # 主体为 Query
        # 子函数 下面的调用都是 最后返回Query
        # SQL语句 first() all() 到数据库的查询语句
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
