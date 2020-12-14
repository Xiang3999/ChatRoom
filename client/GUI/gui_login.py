import tkinter as TK
from tkinter import messagebox
from common import mesg_type
import client.memory
from client.GUI.gui_register import RegisterForm
from client.GUI.gui_contacts import ContactsForm
from tkinter import *
from tkinter import Toplevel
import client.event_handle
from common.net import send11


class LoginForm(TK.Frame):
    def remove_socket_listener_and_close(self):
        client.event_handle.client_listen.remove_listener(self.socket_listener)
        self.master.destroy()

    def destroy_window(self):
        client.memory.tk_root.destroy()

    def socket_listener(self, data):
        if data['type'] == mesg_type.MessageType.login_failed:
            messagebox.showerror('登入失败', '登入失败，请检查用户名密码')
            return

        if data['type'] == mesg_type.MessageType.login_successful:
            client.memory.current_user = data['data']
            self.remove_socket_listener_and_close()

            contacts = Toplevel(client.memory.tk_root, takefocus=True)
            ContactsForm(contacts)

            return

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.resizable(width=False, height=False)
        master.geometry('400x200')
        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")

        self.username = Entry(self)
        self.password = Entry(self, show="*")
        # grid是布局函数，sticky 对齐方式
        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)
        self.username.grid(row=0, column=1, pady=(10, 6))
        self.password.grid(row=1, column=1, pady=(0, 6))

        self.buttonframe = Frame(self)
        self.buttonframe.grid(row=2, column=0, columnspan=2, pady=(4, 6))

        self.logbtn = Button(self.buttonframe, text="Log In", command=self.do_login)
        self.logbtn.grid(row=0, column=0)

        self.registerbtn = Button(self.buttonframe, text="Sign up", command=self.show_register)
        self.registerbtn.grid(row=0, column=1)

        self.pack()
        self.master.title("CHAT ROOM BY PAO")

        self.s = client.memory.socket
        client.event_handle.client_listen.add_listener(self.socket_listener)

    def do_login(self):
        username = self.username.get()
        password = self.password.get()
        if not username:
            messagebox.showerror("出错了", "用户名不能为空")
            return
        if not password:
            messagebox.showerror("出错了", "密码不能为空")
            return

        send11(self.s, mesg_type.MessageType.login, [username, password])

    def show_register(self):
        register_form = Toplevel()
        RegisterForm(register_form)