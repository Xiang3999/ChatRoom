import socket
from common.config import get_config
import json
import time


def connection_To_Server():
    config = get_config()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config['client']['server_ip'], int(config['client']['server_port'])))
    s.send("1".encode("utf-8"))
    ack = s.recv(10).decode('utf-8')
    if ack == "2":
        s.send("3".encode("utf-8"))
        print("connection successful!")
    else:
        print("error")
        return 0
    return s


def connection_To_Client(s):
    conn, addr = s.accept()
    syn = conn.recv(10).decode("utf-8")
    conn.send("2".encode('utf-8'))
    conn.recv(10)
    print(str(conn))
    return conn


def recv11(s):
    return json.loads(s.recv(5120).decode("utf-8"))

    # 这里接送大文件需要检测包的顺序


def recv_bigdata(s):
    return "ok"


def send11(so, type, data=None):
    dir = {
        'type': type,
        'data': data
    }
    packet = json.dumps(dir)
    time.sleep(0.009)
    so.send(packet.encode('utf-8'))
