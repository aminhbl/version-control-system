import math
import os
import socket
import sys
from client_parser import parseInput
from git_manager import push_client_side

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
            toSendMessage = parseInput(message)
            if toSendMessage == "":
                print("Invalid input!!!")
                continue
            s.sendall(str(len(toSendMessage.encode('utf-8'))).encode('ascii'))
            s.sendall(toSendMessage.encode('ascii'))

            data = s.recv(2048)
            data = data.decode("ascii")
            string_data = ""
            for i in range(math.ceil(int(data) / 2048)):
                temp = s.recv(2048).decode()
                string_data = string_data + str(temp)

            if string_data.startswith("pull_request"):
                string_data = string_data[12:]
                push_client_side(string_data, "./")
                print("pull successful!")
            else:
                print('Received from the server:\n', string_data)
            if message == 'stop':
                break

    except socket.error:
        print('Shit hit the fan!')
    finally:
        s.close()


if __name__ == '__main__':
    local_dir = input("Enter you Local directory: ")
    os.chdir(local_dir)
    client()
