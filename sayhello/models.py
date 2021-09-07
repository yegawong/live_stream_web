# -*- coding: utf-8 -*-
"""
    :author: (Yega)
    :copyright: © 2021 yega
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime

from sayhello import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(200))
    pid = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Adress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tuiliu = db.Column(db.String(200))
    rtmp = db.Column(db.String(200))
    flv = db.Column(db.String(200))
    m3u8 = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
