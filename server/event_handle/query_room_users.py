# -*- coding: utf-8 -*-
# @Time : 2020/12/14 20:41 
# @Author : PAO 
# @File : query_room_users.py
from common.mesg_type import MessageType
from server.server_function.memory import *
import server.database as database
from common.net import send11


def run(s, data):
    user_id = client_to_user_id[s]
    if not database.in_room(user_id, data):
        send11(s, MessageType.general_failure, '不在群里')
        return
    send11(s, MessageType.query_room_users_result, [database.get_room_members(data), data])
