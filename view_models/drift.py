# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/25 20:52
# @Author : '红文'
# @File : drift.py
# @Software: PyCharm
from app.libs.enums import PendingStatus


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}

        self.__parse(drift, current_user_id)

    def _parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}

        self.data = self._parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)

        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
        }
        return r