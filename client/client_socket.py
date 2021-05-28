import math
import os
import socket
import sys
from client.client_parser import build_message
from server.git_manager import push_client_side

HOST = "127.0.0.1"
PORT = 8000


def client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Unable to connect to the server')
        sys.exit(-1)
    try:
        s.connect((HOST, PORT))
        while True:
            message = input()
            toSendMessage = build_message(message)
            if toSendMessage is None:
                continue
            s.sendall(str(len(toSendMessage.encode('utf-8'))).encode('ascii'))
            s.sendall(toSendMessage.encode('ascii'))

            data = s.recv(2048)
            data = data.decode("ascii")
            string_data = ""
            for i in range(math.ceil(int(data) / 2048)):
                temp = s.recv(2048)
                temp = temp.decode()
                string_data = string_data + str(temp)

            if string_data.startswith("pull#"):
                string_data = string_data[5:]
                push_client_side(string_data, "./")
                print('Pull successful')
            else:
                print('$', string_data)
            if message == 'stop':
                break

    except socket.error:
        print('Connection was disturbed!')
    finally:
        s.close()


if __name__ == '__main__':
    # C:/Users/Amin/Desktop/C/dns
    local_dir = input("Enter you Local directory: ")
    os.chdir(local_dir)
    client()
