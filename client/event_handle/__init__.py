import select

from tkinter import messagebox
from common.mesg_type import MessageType
import client.memory
import  struct
import  sys
import traceback  # 异常处理包

callback_funcs=[]

#[{target_id,target_type,func}]
message_listeners=[]

class client_listen:
    def __init__(self,s,root):
        self.scoket=s
        self.tk_root=root
        self.start_listen_thread()
    def start_listen_thread(self):
        mesg_recv=0
        mesg_send=0
        data_buffer=bytes()
        while True:
            rlist,wlist,xlist=select.select([self.scoket],[],[])
            if len(rlist):
                if mesg_send==0 and mesg_recv==0:
                    # 一次新的连接
                    flag=True
                    first_4_bytes = ''
                    try:
                        first_4_bytes = self.scoket.recv(4)
                    except ConnectionError:
                        flag = False
                    if first_4_bytes == "" or len(first_4_bytes) < 4:
                        flag = False

                    if not flag:
                        # 服务器已经关闭了
                        self.tk_root.destory()
                        a=1
                    else:
                        data_buffer=bytes()
                # 接受数据
                buffer=self.scoket.recv(1024)




