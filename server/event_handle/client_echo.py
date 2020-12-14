# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 11:41 
# @Author : PAO 
# @File : client_echo.py
from common.mesg_type import MessageType
from common.net import send11


def run(s, data):
    send11(s, MessageType.server_echo, data)
