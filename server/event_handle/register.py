# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 11:41 
# @Author : PAO 
# @File : register.py
from common.mesg_type import MessageType
from server.database import *
from common.net import send11
from hashlib import md5


def run(s, data):
    data[0] = data[0].strip().lower()
    c = get_cursor()
    r = c.execute('SELECT * from users where username=?', [data[0]])
    rows = r.fetchall()
    if len(rows) > 0:
        send11(s, MessageType.username_taken)
        return

    c = get_cursor()
    c.execute('INSERT into users (username,password,nickname) values (?,?,?)',
              [data[0], to_md5(data[1]), data[2]])
    send11(s, MessageType.register_successful, c.lastrowid)


def to_md5(text):
    m = md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()
