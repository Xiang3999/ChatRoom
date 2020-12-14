# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 20:39 
# @Author : PAO 
# @File : send_message.py
from common.mesg_type import MessageType
from server.server_function.memory import *
import server.database as database
from common.net import send11
import time


# {target_type:int(0=私聊 1=群聊),target_id:int,message:str}

def run(s, data):
    user_id = client_to_user_id[s]
    sender = database.get_user(user_id)

    # target只是dispatch用

    # target_id延后做，对于发送方和接收方不一样
    message = {"message": data['message'], 'sender_id': user_id,
               'sender_name': sender['nickname'],
               'target_type': data['target_type'],
               'time': int(round(time.time() * 1000))}

    if data['target_type'] == 0:
        # 私聊
        if not database.is_friend_with(user_id, data['target_id']):
            send11(s, MessageType.general_failure, '还不是好友')
            return

        # 给发送方发回执
        message['target_id'] = data['target_id']
        send11(user_id_to_sc[user_id], MessageType.on_new_message, message)
        database.add_to_chat_history(user_id, message['target_id'], message['target_type'],
                                     message, True)

        # 给接收方发消息，存入聊天记录
        message['target_id'] = user_id
        sent = False
        if data['target_id'] in user_id_to_sc:
            sent = True
            send11(user_id_to_sc[data['target_id']], MessageType.on_new_message, message)

        database.add_to_chat_history(data['target_id'], message['target_id'], message['target_type'],
                                     message, sent)

    if data['target_type'] == 1:
        # 群聊
        message['target_id'] = data['target_id']

        if not database.in_room(user_id, data['target_id']):
            send11(s, MessageType.general_failure, '还没有加入该群')
            return

        users_id = database.get_room_members_id(data['target_id'])

        for user_id in users_id:
            sent = False
            if user_id in user_id_to_sc:
                send11(user_id_to_sc[user_id], MessageType.on_new_message, message)
                sent = True

            database.add_to_chat_history(user_id, message['target_id'], message['target_type'],
                                         message, sent)
