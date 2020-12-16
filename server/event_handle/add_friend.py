# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 11:40 
# @Author : PAO 
# @File : add_friend.py
from common.mesg_type import MessageType
from server.server_function.memory import *
import server.database as database
from common.net import send11


def run(s, data):
    user_id = client_to_user_id[s]
    # data = username
    c = database.get_cursor()
    username = data.strip().lower()
    r = c.execute('SELECT user_id from users where username=?', [username]).fetchall()
    if len(r) == 0:
        send11(s, MessageType.add_friend_result, [False, '用户名不存在'])
        return

    uid = r[0][0]

    if uid == user_id:
        send11(s, MessageType.add_friend_result, [False, '不能加自己为好友'])
        return

    c = database.get_cursor()
    r = c.execute('SELECT 1 from friends where from_user_id=? and to_user_id=?', [user_id, uid]).fetchall()

    if len(r) != 0:
        send11(s, MessageType.add_friend_result, [False, '已经是好友/已经发送过好友请求'])
        return

    c = database.get_cursor()
    c.execute('insert into friends (from_user_id,to_user_id,accepted) values (?,?,0)', [user_id, uid]).fetchall()

    send11(s, MessageType.add_friend_result, [True, ''])

    if uid in user_id_to_sc:
        send11(user_id_to_sc[uid], MessageType.incoming_friend_request, database.get_user(user_id))
