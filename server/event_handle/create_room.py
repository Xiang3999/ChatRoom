# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 20:41 
# @Author : PAO 
# @File : create_room.py

from common.mesg_type import MessageType
from server.server_function.memory import *
import server.database as database
from server.event_handle import *
from common.net import send11


def run(s, data):
    user_id = client_to_user_id[s]
    c = database.get_cursor()
    c.execute("insert into chat_room (room_name) values (?)", [data])
    send11(s, MessageType.contact_info, add_target_type3(database.get_room(c.lastrowid), 1))
    database.add_to_room(user_id, c.lastrowid)
    send11(s, MessageType.general_msg, '创建成功，群号为：' + str(c.lastrowid))


def add_target_type3(obj, type):
    obj['type'] = type
    return obj
