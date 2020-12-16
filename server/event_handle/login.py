# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 11:31 
# @Author : PAO 
# @File : login.py

from common.mesg_type import MessageType

import server.database as database
from server.event_handle import *
from server.server_function.memory import *
from common.net import *
from hashlib import md5


def run(s, data):
    data[0] = data[0].strip().lower()
    c = database.get_cursor()
    r = c.execute('SELECT user_id,username from users where username=? and password=?', (data[0], to_md5(data[1])))
    rows = r.fetchall()

    if len(rows) == 0:
        # 登陆失败
        send11(s, MessageType.login_failed)
        return

    user_id = rows[0][0]

    # 已经登入，踢下线
    if user_id in user_id_to_sc:
        sc_old = user_id_to_sc[user_id]
        send11(sc_old, MessageType.server_kick)
        sc_old.close()
        remove_c_from_client_list(sc_old)

    client_to_user_id[s] = user_id
    user_id_to_sc[user_id] = s
    user = database.get_user(user_id)
    send11(s, MessageType.login_successful, user)

    login_bundle = {}

    # 发送群列表
    rms = database.get_user_rooms(user_id)
    login_bundle['rooms'] = list(map(lambda x: add_target_type4(x, 1), rms))

    # for rm in rms:
    #     sc.send(MessageType.contact_info, add_target_type(rm, 1))

    # 发送好友请求
    frs = database.get_pending_friend_request(user_id)

    for fr in frs:
        send11(s, MessageType.incoming_friend_request, fr)

    # 发送好友列表
    frs = database.get_friends(user_id)
    login_bundle['friends'] = list(map(lambda x: add_target_type4(x, 0), frs))
    # 通知他的好友他上线了
    for fr in frs:
        if fr['user_id'] in user_id_to_sc:
            send11(user_id_to_sc[fr['user_id']], MessageType.friend_online_state, [True, user_id])

    # 通知群聊里的人他上线了
    # [room_id, user_id, online]
    rooms_id = database.get_user_rooms_id(user_id)
    for room_id in rooms_id:
        users_id = database.get_room_members_id(room_id)
        for _user_id in users_id:
            if _user_id in user_id_to_sc and user_id != _user_id:
                send11(user_id_to_sc[_user_id], MessageType.room_user_on_off_line,
                       [room_id, user_id, True])

    login_bundle['messages'] = database.get_chat_history(user_id)
    send11(s, MessageType.login_bundle, login_bundle)


def to_md5(text):
    m = md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


def add_target_type4(obj, type):
    obj['type'] = type
    return obj
