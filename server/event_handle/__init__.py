# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 11:31 
# @Author : PAO 
# @File : __init__.py.py
import server.event_handle.login
import server.event_handle.send_message
import server.event_handle.register
import server.event_handle.resolve_friend_request
import server.event_handle.client_echo
import server.event_handle.add_friend
import server.event_handle.join_room
import server.event_handle.create_room
import server.event_handle.query_room_users
import server.event_handle.bad
from common.mesg_type import MessageType
from hashlib import md5

event_handle_map = {
    MessageType.login: login,
    MessageType.send_message: send_message,
    MessageType.register: register,
    MessageType.resolve_friend_request: resolve_friend_request,
    MessageType.client_echo: client_echo,
    MessageType.add_friend: add_friend,
    MessageType.join_room: join_room,
    MessageType.create_room: create_room,
    MessageType.query_room_users: query_room_users,
    MessageType.bad: bad,
}


def handle_event(s, event_type, data):
    event_handle_map[event_type].run(s, data)


def add_target_type(obj, type):
    obj['type'] = type
    return obj
