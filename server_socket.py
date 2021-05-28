import math
import socket
import threading
from copy import deepcopy
import server_parser
from git_manager import authenticate_user

HOST = "127.0.0.1"
PORT = 8000


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("Server is on!")
        while True:
            s.listen(1)
            connection, address = s.accept()
            new_thread = ClientHandler(address, connection)
            new_thread.start()


class ClientHandler(threading.Thread):
    def __init__(self, address, client_socket):
        threading.Thread.__init__(self)
        self.connection = client_socket
        self.address = address
        print("connection established with: ", address)

    def run(self):
        username = password = current_repository = None
        while True:
            data_size = self.connection.recv(2048)
            data_size = data_size.decode()
            string_data = ""
            for i in range(math.ceil(int(data_size) / 2048)):
                rec = self.connection.recv(2048).decode()
                string_data = string_data + str(rec)
            if not string_data:
                break

            if username is not None:
                user = authenticate_user(username, password)
                answer = server_parser.parseReceivedMessage(string_data, user, current_repository)
            else:
                answer = server_parser.parseReceivedMessage(string_data, None, current_repository)

            if type(answer) == list and len(answer) == 2:
                username = deepcopy(answer[0])
                password = deepcopy(answer[1])
                answer = "User logged in"
            if type(answer) == list and len(answer) == 1:
                current_repository = answer[0]
                answer = "Repository selected :)"

            if answer is None:
                answer = "ERROR!"

            self.connection.sendall(str(len(answer.encode('utf-8'))).encode('ascii'))
            self.connection.sendall(bytes(answer, 'UTF-8'))

        self.connection.close()
        print("client at ", self.address, " disconnected.")


if __name__ == '__main__':
    server()
