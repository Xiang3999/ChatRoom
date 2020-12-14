# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 19:22 
# @Author : PAO 
# @File : gui_contacts.py
import tkinter as tk
from tkinter import messagebox
from common.mesg_type import MessageType
import client.memory
from tkinter import *
from client.components.vertical_scrolled_frame import VerticalScrolledFrame
from client.components.contact_item import ContactItem
from client.GUI.gui_chat import ChatForm
from tkinter import Toplevel
import datetime
import client.event_handle
from tkinter import simpledialog
from common.net import *


class ContactsForm(tk.Frame):
    bundle_process_done = False

    def remove_socket_listener_and_close(self):
        client.event_handle.client_listen.remove_listener(self.socket_listener)
        self.master.destroy()
        client.memory.tk_root.destroy()

    def socket_listener(self, frame):
        if frame['type'] == MessageType.login_bundle:
            bundle = frame['data']
            friends = bundle['friends']
            rooms = bundle['rooms']
            messages = bundle['messages']
            for friend in friends:
                self.handle_new_contact(friend)
            for room in rooms:
                self.handle_new_contact(room)
            for item in messages:
                # [[data:bytes,sent:int]]
                sent = item[1]
                message = item[0]
                client.event_handle.client_listen.deal_packet(message, not sent)

            self.bundle_process_done = True
            self.refresh_contacts()

        if frame['type'] == MessageType.incoming_friend_request:
            result = messagebox.askyesnocancel("好友请求", frame['data']['nickname'] + "请求加您为好友，是否同意？(按Cancel为下次再询问)");
            if result == None:
                return
            self.s.send(MessageType.resolve_friend_request, [frame['data']['id'], result])

        if frame['type'] == MessageType.contact_info:
            self.handle_new_contact(frame['data'])
            return

        if frame['type'] == MessageType.add_friend_result:
            if frame['data'][0]:
                messagebox.showinfo('添加好友', '好友请求已发送')
            else:
                messagebox.showerror('添加好友失败', frame['data'][1])
            return

        if frame['type'] == MessageType.friend_on_off_line:
            friend_user_id = frame['data'][1]

            for i in range(0, len(self.contacts)):
                if self.contacts[i]['id'] == friend_user_id and self.contacts[i]['type'] == 0:
                    self.contacts[i]['online'] = frame['data'][0]
                    break

            self.refresh_contacts()
            return

    def handle_new_contact(self, data):
        data['last_timestamp'] = 0
        data['last_message'] = '(没有消息)'
        self.contacts.insert(0, data)
        self.refresh_contacts()

    def on_frame_click(self, e):
        item_id = e.widget.item['id']
        if item_id in client.memory.window_instance[e.widget.item['type']]:
            client.memory.window_instance[e.widget.item['type']][item_id].master.deiconify()
            return
        form = Toplevel(client.memory.tk_root, takefocus=True)
        client.memory.window_instance[e.widget.item['type']][item_id] = ChatForm(e.widget.item, form)

    def on_add_friend(self):
        result = simpledialog.askstring('添加好友', '请输入用户名')
        if (not result):
            return
        send11(self.s, MessageType.add_friend, result)

    def on_add_room(self):
        result = simpledialog.askinteger('添加群', '请输入群号')
        if (not result):
            return
        send11(self.s, MessageType.join_room, result)

    def on_create_room(self):
        result = simpledialog.askstring('创建群', '请输入群名称')
        if (not result):
            return
        send11(self.s, MessageType.create_room, result)

    class my_event:
        widget = None

        def __init__(self, widget):
            self.widget = widget

    def try_open_user_id(self, id, name, username):

        for i in range(0, len(self.pack_objs)):
            frame = self.pack_objs[i]
            if frame.item['id'] == id and frame.item['type'] == 0:
                self.on_frame_click(self.my_event(frame))
                return
        result = messagebox.askyesno("是否加好友", name + "不在您的好友列表中，是否加好友？")
        if result:
            send11(self.s, MessageType.add_friend, username)

    pack_objs = []

    def refresh_contacts(self):
        if not self.bundle_process_done:
            return
        for pack_obj in self.pack_objs:
            pack_obj.pack_forget()
            pack_obj.destroy()

        self.pack_objs = []

        # sorted(self.contacts, cmp=compare)
        self.contacts.sort(key=lambda x: -client.memory.last_message_timestamp[x['type']].get(x['id'], 0))
        for item in self.contacts:
            contact = ContactItem(self.scroll.interior, self.on_frame_click)
            contact.pack(fill=BOTH, expand=True)
            contact.item = item

            contact.bind("<Button>", self.on_frame_click)
            if (item['type'] == 0):
                # 联系人
                contact.title.config(text=item['nickname'] + (' (在线)' if item['online'] else ' (离线)'))
                contact.title.config(fg='green' if item['online'] else '#999')
            if (item['type'] == 1):
                # 群
                contact.title.config(text='[群:' + str(item['id']) + '] ' + item['room_name'])
                contact.title.config(fg='blue')

            # contact.last_message.config(text=item['nickname'] + (' (在线)' if item['online'] else ' (离线)'))

            self.pack_objs.append(contact)
            time_message = datetime.datetime.fromtimestamp(
                item['last_timestamp']
            ).strftime('%Y-%m-%d %H:%M:%S')

            contact.last_message_time.config(text=time_message)

            contact.last_message.config(text=client.memory.last_message[item['type']].get(item['id'], '(没有消息)'))
            contact.last_message_time.config(text=datetime.datetime.fromtimestamp(
                int(client.memory.last_message_timestamp[item['type']].get(item['id'], 0)) / 1000
            ).strftime('%Y-%m-%d %H:%M:%S'))

            unread_count = client.memory.unread_message_count[item['type']].get(item['id'], 0)
            contact.unread_message_count.pack_forget()
            if unread_count != 0:
                contact.last_message.pack_forget()
                contact.unread_message_count.pack(side=RIGHT, anchor=E, fill=None, expand=False, ipadx=4)
                contact.last_message.pack(side=LEFT, fill=X, expand=True, anchor=W)
                contact.unread_message_count.config(text=str(unread_count))

    def __init__(self, master=None):
        client.memory.contact_window.append(self)
        super().__init__(master)
        self.master = master
        screen_width = client.memory.tk_root.winfo_screenwidth()
        screen_height = client.memory.tk_root.winfo_screenheight()
        x = screen_width - 300
        y = (screen_height / 2) - 400
        master.geometry('%dx%d+%d+%d' % (260, 600, x, y))
        self.scroll = VerticalScrolledFrame(self)
        self.scroll.pack(fill=BOTH, expand=True)
        self.pack(side=TOP, fill=BOTH, expand=True)

        self.button_frame = Frame(self)

        self.add_friend = Button(self.button_frame, text="添加好友", command=self.on_add_friend)
        self.add_friend.pack(side=LEFT, expand=True, fill=X)

        self.add_room = Button(self.button_frame, text="添加群", command=self.on_add_room)
        self.add_room.pack(side=LEFT, expand=True, fill=X)

        self.create_room = Button(self.button_frame, text="创建群", command=self.on_create_room)
        self.create_room.pack(side=LEFT, expand=True, fill=X)

        self.button_frame.pack(expand=False, fill=X)

        self.contacts = []

        self.master.title(client.memory.user_inf['nickname'] + " - 联系人列表")
        self.s = client.memory.socket
        client.event_handle.client_listen.add_listener(self.socket_listener)
        master.protocol("WM_DELETE_WINDOW", self.remove_socket_listener_and_close)
