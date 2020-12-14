# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 11:41 
# @Author : PAO 
# @File : join_room.py
from common.mesg_type import MessageType
from server.server_function.memory import *
import server.database as database
from common.net import send11
from server.event_handle import *


def run(s, data):
    user_id = client_to_user_id[s]
    if database.in_room(user_id, data):
        send11(s, MessageType.general_failure, '已经在群里了')
        return
    room = database.get_room(data)
    if room is None:
        send11(s, MessageType.general_failure, '群不存在')
        return
    database.add_to_room(user_id, data)
    send11(s, MessageType.contact_info, add_target_type(room, 1))
