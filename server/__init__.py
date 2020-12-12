#!/usr/bin/env python
import socket
from common.config import get_config
from common.mesg_type import  *
from common.net import *
import json
import threading
import select
from  server.server_function.remove_c_from_client_list import *
from server.database import *

class ChatServer:
    def __init__(self):
        self.server_socket = None
        self.mesg_send={}
        self.mesg_recv={}
        self.data_buffer=bytes()
        self.create_server()
    """
    """
    def create_server(self):

        # 读取配置文件
        config = get_config()
        local_ip = config['server']['bind_ip']
        local_port = config['server']['bind_port']
        # socket 初始化
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # socket 绑定
        self.server_socket.bind((local_ip, local_port))
        print("Server listening on " + config['server']['bind_ip'] + ":" +
              str(config['server']['bind_port']))
        self.server_socket.listen(5)

        self.event_handle()


    def event_handle(self):

        s=self.server_socket
        while True:
            rlist, wlist, xlist = select.select(list(client_list) + [s], [], [])
            for i in rlist:
                # 监听socket为readable，说明有新的客户要连入
                if i == s:
                    client_s=connection_To_Client(s)
                    client_dict[client_s]=client_s
                    client_list.append(client_s)
                    self.mesg_recv[client_s]=0
                    self.mesg_send[client_s]=0
                   # self.data_buffer[client_s]=0
                    continue
                # 如果不监听socket,就是以前连接的客户发来的消息
                client_s=client_dict[i]

                if self.mesg_recv[client_s]==0 and self.mesg_send[client_s]==0:
                    # 新的接受
                    flag=True
                    first_4_bytes=''
                    try:
                        first_4_bytes=client_s.recv(4)
                    except ConnectionError:
                        flag=False
                    if first_4_bytes=="" or len(first_4_bytes)<4:
                        flag=False

                    if not flag:
                        client_s.close()
                        # client_to_user_id 是
                        if client_s in client_to_user_id:
                            # 通知他好友，他下线了 friend_offline
                            user_id = client_to_user_id[client_s]
                            friends=database.get_friends(user_id)
                            for friend in friends:
                                if friend['id'] in user_id_to_sc:
                                    self._send(user_id_to_sc[friend['id']],
                                               MessageType.friend_online_state,"0"+user_id)
                            # 获取群号，通知群成员他下线了
                            rooms_id=database.get_user_rooms_id(user_id)
                            for room_id in rooms_id:
                                # 获取群成员
                                fris_id= database.get_room_members_id(room_id)
                                for fri_id in fris_id:
                                    if fri_id in user_id_to_sc and fri_id!=user_id:
                                        self._send(user_id_to_sc[fri_id],
                                                   MessageType.room_user_on_off_line,"0"+user_id)
                        # 移除列表
                        remove_c_from_client_list(client_s)


    def _send(self,so,type,data):
        dir={
            'type':type,
            'data':data,
        }
        packet = json.dumps(dir)
        so.send(packet.encode('utf-8'))
        print("send mesg: " + packet)

ChatServer()








