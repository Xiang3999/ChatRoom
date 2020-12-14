import threading
import tkinter as TK
import _thread
from tkinter import messagebox
from client.event_handle import *
from client.GUI.gui_login import  LoginForm
from common.net import connection_To_Server
import client.memory

def start():
    root=TK.Tk()
    client.memory.tk_root=root

    try:
        client.memory.socket=connection_To_Server()
    except:
        messagebox.showerror("Error","Can not connect to the server !")
        exit(1)
    thread = threading.Thread(target=client_listen, args=(client.memory.socket,root,))
    thread.start()

    login = TK.Toplevel()
    LoginForm(login)

    root.withdraw()
    root.mainloop()

    #异常处理
    try:
       root.destroy()
    except TK.TclError:
       pass
#quit()停止TCL解释器，是在大多数情况下你想要的，因为你的tkinter应用程序也将停止，
#idle本身是一个tkinker应用程序，因此，如果你在应用程序中调用quit()，并且TCL解释器被终止
#，那么idle也将终止。destroy()只终止主循环并删除所有小部件，如果你从另一个Tkinter应用程
#序调用你的应用程序，或者如果你有多个主循环，它更安全。
