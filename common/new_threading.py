import threading
def receive_message_in_a_new_thread(self):
    while True:
        client = so, (ip, port) = self.server_socket.accept()
        # self.add_to_clients(client)
        print('Connected to ', ip, ':', str(port))
        t = threading.Thread(target=self.recv_mesg, args=(so,))
        t.start()