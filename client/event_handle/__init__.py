import select
import json
from tkinter import messagebox
from pprint import pprint
from common.mesg_type import MessageType
import client.memory
import  struct
import  sys
import traceback  # 异常处理包

callback_funcs=[]

#[{target_id,target_type,func}]
message_listeners = []
func_to_tuple = {}
class client_listen:
    def __init__(self,s,root):
        self.scoket=s
        self.tk_root=root
        self.start_listen_thread()
    def start_listen_thread(self):
        mesg_recv=0
        mesg_send=0
        data_buffer = bytes()
        frame = ""
        while True:
            rlist,wlist,xlist=select.select([self.scoket],[],[])
            if len(rlist):
                if mesg_send==0 and mesg_recv==0:
                    # 一次新的连接
                    flag = True
                    try:
                        frame = self._recv(self.scoket)
                    except ConnectionError:
                        flag = False
                    if not flag:
                        # 服务器已经关闭了
                        self.tk_root.destory()
                # 接受数据
                # ata_buffer+=bytes(frame['data'])
                if int(frame['type']) == MessageType.long_mesg:
                    frame = self._recv_bigdata(self.scoket)
                elif frame != "":
                    try:
                        data = frame
                        type = int(data['type'])
                        # 处理general failure
                        if type == MessageType.general_failure:
                            messagebox.showerror("出错了", data['data'])

                        # 处理general message
                        if type == MessageType.general_msg:
                            messagebox.showinfo("消息", data['data'])

                        if type == MessageType.server_kick:
                            messagebox.showerror("出错了", '您的账户在别处登入')
                            client.memory.tk_root.destroy()

                        if type == MessageType.server_echo:
                            pprint(['server echo', data['data']])

                        # 处理on_new_message
                        if type == MessageType.on_new_message:
                            self.deal_packet(data['data'])

                        for func in callback_funcs:
                            func(data)

                    except:
                        pprint(sys.exc_info())
                        traceback.print_exc(file=sys.stdout)
                        pass

    def gen_last_message(obj):
        # type 0 - 文字消息 1 - 图片消息
        prefix = ''
        if obj['target_type'] == 1:
            return obj['sender_name'] + ':' + '[图片消息]'
        if obj['target_type'] == 0:
            return obj['sender_name'] + ':' + obj['message'].replace('\n', ' ')

    def _recv(self, s):
        return json.loads(s.recv(1024).decode("utf-8"))

    def _recv_bigdata(self, s):
        return "ok"

    def deal_packet(self, packet, update_unread_count=True):
        # 放入 chat_history
        if packet['target_id'] not in client.memory.chat_history[
            packet['target_type']]:
            client.memory.chat_history[packet['target_type']][packet['target_id']] = []
        client.memory.chat_history[packet['target_type']][packet['target_id']].append(packet)
        # 更新 last_message
        client.memory.last_message[packet['target_type']][packet['target_id']] = self.gen_last_message(packet)
        # 更新 last_message_timestamp
        client.memory.last_message_timestamp[packet['target_type']][
            packet['target_id']] = packet['time']
        # 更新 unread_message_count
        if packet['target_id'] not in client.memory.unread_message_count[
            packet['target_type']]:
            client.memory.unread_message_count[packet['target_type']][
                packet['target_id']] = 0
        if packet['target_id'] not in client.memory.window_instance[
            packet['target_type']]:
            if update_unread_count:
                client.memory.unread_message_count[packet['target_type']][
                    packet['target_id']] += 1

        # 更新contacts
        client.memory.contact_window[0].refresh_contacts()
        # 通知聊天窗口
        for item in message_listeners:
            if item['target_type'] == packet['target_type'] and item['target_id'] == \
                    packet['target_id']:
                item['func'](packet)

    def add_listener(self, func):
        callback_funcs.append(func)

    def remove_listener(self, func):
        callback_funcs.remove(func)

    def add_message_listener(self, target_type, target_id, func):
        func_to_tuple[func] = {'target_type': target_type, 'target_id': target_id, 'func': func}
        message_listeners.append(func_to_tuple[func])

    def remove_message_listener(self, func):
        if func in func_to_tuple:
            message_listeners.remove(func_to_tuple[func])
