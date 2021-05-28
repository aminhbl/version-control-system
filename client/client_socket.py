import math
import os
import socket
import sys
from client.client_parser import build_message
from server.git_manager import push_client_side


class Client:
    def __init__(self, port, host, curr_dir):
        self.port = port
        self.host = host
        self.online = True
        self.curr_dir = curr_dir
        os.chdir(curr_dir)

    def change_dir(self):
        os.chdir(self.curr_dir)

    def run(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Unable to connect to the server')
            sys.exit(-1)
        try:
            s.connect((self.host, self.port))
            while self.online:
                message = input()
                formatted_message = build_message(message)
                if formatted_message.startswith("cd"):
                    self.curr_dir = formatted_message[2:]
                    self.change_dir()
                    continue
                if formatted_message is None:
                    continue
                s.sendall(str(len(formatted_message.encode('utf-8'))).encode('ascii'))
                s.sendall(formatted_message.encode('ascii'))

                rec_message = ""
                message_size = s.recv(2048).decode("ascii")
                for i in range(math.ceil(int(message_size) / 2048)):
                    message_part = s.recv(2048).decode()
                    rec_message = rec_message + str(message_part)

                if rec_message.startswith("pull#"):
                    rec_message = rec_message[5:]
                    push_client_side(rec_message, "./")
                    print('Pull successful')
                else:
                    print('$', rec_message)
                if rec_message == 'stop':
                    self.online = False

        except socket.error:
            print('Connection was disturbed!')
        finally:
            s.close()


if __name__ == '__main__':
    client = Client(8000, "127.0.0.1", 'C:/Users/Amin/Desktop/C/dns')
    client.run()
