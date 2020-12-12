import socket
from common.config import get_config
def connection_To_Server():
    config=get_config()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config['client']['server_ip'], int(config['client']['server_port'])))
    s.send("1".encode("utf-8"))
    ack=s.recv(10).decode('utf-8')
    if ack=="2":
        s.send("3".encode("utf-8"))
        print("connection successful!")
    else:
        print("error")
        return 0
    return s

def connection_To_Client(s):
    conn,addr=s.accept()
    syn=conn.recv(10).decode("utf-8")
    conn.send("2".encode('utf-8'))
    conn.recv(10)
    print(str(conn))
    return conn






