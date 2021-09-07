# -*- coding: utf-8 -*-
"""
    :author: (Yega)
    :copyright: © 2021 yega
    :license: MIT, see LICENSE for more details.
"""
import re
import time
import hashlib
import datetime
from sayhello.models import Adress
from sayhello import db


def md5sum(src):
    m = hashlib.md5()
    m.update(src)
    return m.hexdigest()


def a_auth(uri, key, exp):
    p = re.compile("^(rtmp://)?([^/?]+)(/[^?]*)?(\\?.*)?$")
    if not p:
        return None
    m = p.match(uri)
    scheme, host, path, args = m.groups()
    if not scheme:
        scheme = "rtmp://"
    if not path:
        path = "/"
    if not args:
        args = ""
    rand = "0"  # "0" by default, other value is ok
    uid = "0"  # "0" by default, other value is ok
    sstring = "%s-%s-%s-%s-%s" % (path, exp, rand, uid, key)
    hashvalue = md5sum(sstring.encode('utf-8'))
    auth_key = "%s-%s-%s-%s" % (exp, rand, uid, hashvalue)
    if args:
        return "%s%s%s%s&auth_key=%s" % (scheme, host, path, args, auth_key)
    else:
        return "%s%s%s%s?auth_key=%s" % (scheme, host, path, args, auth_key)


def a_auth_tls(uri, key, exp):
    p = re.compile("^(http://)?([^/?]+)(/[^?]*)?(\\?.*)?$")
    if not p:
        return None
    m = p.match(uri)
    scheme, host, path, args = m.groups()
    if not scheme:
        scheme = "http://"
    if not path:
        path = "/"
    if not args:
        args = ""
    rand = "0"  # "0" by default, other value is ok
    uid = "0"  # "0" by default, other value is ok
    sstring = "%s-%s-%s-%s-%s" % (path, exp, rand, uid, key)
    hashvalue = md5sum(sstring.encode('utf-8'))
    auth_key = "%s-%s-%s-%s" % (exp, rand, uid, hashvalue)
    if args:
        return "%s%s%s%s&auth_key=%s" % (scheme, host, path, args, auth_key)
    else:
        return "%s%s%s%s?auth_key=%s" % (scheme, host, path, args, auth_key)


def auth():
    app_name = 'app_name'
    stream_name = 'stream_name'
    push_domain = "push_domain"
    pull_domain = "pull_domain"
    uri = "rtmp://" + push_domain + "/" + \
        app_name + "/" + stream_name  # original uri
    rtmp_uri = "rtmp://" + pull_domain + "/" + \
        app_name + "/" + stream_name  # original uri
    flv_uri = "http://" + pull_domain + "/" + app_name + \
        "/" + stream_name + ".flv"  # original uri
    m3u8_uri = "http://" + pull_domain + "/" + app_name + \
        "/" + stream_name + ".m3u8"  # original uri
    key = "key"  # private key of     authorization
    # expiration     time: 1 hour after current itme
    exp = int(time.time()) + 1 * 14400
    authuri = a_auth(uri, key, exp)  # auth type:
    key = "key"  # private key of     authorization
    # exp = int(time.time()) + 1 * 3600  # expiration     time: 1 hour after current itme
    rtmp_authuri = a_auth(rtmp_uri, key, exp)  # auth type:
    flv_authuri = a_auth_tls(flv_uri, key, exp)  # auth type:
    m3u8_authuri = a_auth_tls(m3u8_uri, key, exp)  # auth type:
    return authuri, rtmp_authuri, flv_authuri, m3u8_authuri


def judge_update():
    adress = Adress.query.all()
    if not adress:
        return True, None
    res = Adress.query.filter_by(id=adress[0].id).first()
    sql_timestamp = res.timestamp
    if sql_timestamp + datetime.timedelta(hours=6) < datetime.datetime.utcnow():
        return True, res
    else:
        return False, res

def generate_adress():
    res, mess = judge_update()
    if res:
        if mess is not None:
            db.session.delete(mess)
            db.session.commit()
        authuri, rtmp_authuri, flv_authuri, m3u8_authuri = auth()
        curr = Adress(tuiliu=authuri, rtmp=rtmp_authuri, flv=flv_authuri, m3u8=m3u8_authuri)
        db.session.add(curr)
        db.session.commit()
        return authuri, rtmp_authuri, flv_authuri, m3u8_authuri
    else:
        return mess.tuiliu, mess.rtmp, mess.flv, mess.m3u8
        

if __name__ == "__main__":
    print(generate_adress())
