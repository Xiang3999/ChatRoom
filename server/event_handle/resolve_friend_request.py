# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 20:40 
# @Author : PAO 
# @File : resolve_friend_request.py
from common.mesg_type import MessageType
from server.server_function.memory import *
import server.database as database
from common.net import send11
from server.event_handle import *


def run(s, data):
    user_id = client_to_user_id[s]

    uid = data[0]
    accepted = data[1]
    c = database.get_cursor()
    r = c.execute('SELECT 1 from friends where from_user_id=? and to_user_id=? and accepted=0', [uid, user_id])
    rows = r.fetchall()
    if len(rows) == 0:
        return

    if not accepted:
        c = database.get_cursor()
        c.execute('delete from friends where from_user_id=? and to_user_id=? and accepted=0', [uid, user_id])
        return

    if accepted:
        c = database.get_cursor()
        c.execute('update friends set accepted=1 where from_user_id=? and to_user_id=? and accepted=0', [uid, user_id])
        c = database.get_cursor()
        c.execute('insert into friends (from_user_id,to_user_id,accepted) values (?,?,1)', [user_id, uid])

        send11(s, MessageType.contact_info, add_target_type1(database.get_user(uid), 0))

        if uid in user_id_to_sc:
            send11(user_id_to_sc[uid], MessageType.contact_info, add_target_type1(database.get_user(user_id), 0))


def add_target_type1(obj, type):
    obj['type'] = type
    return obj
