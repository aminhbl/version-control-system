import math
import socket
import threading
from server import server_parser


class Server:
    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.online = True

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            print("$_$")
            while self.online:
                s.listen(1)
                connection, address = s.accept()
                ThreadHandler(address, connection).start()


class ThreadHandler(threading.Thread):
    def __init__(self, address, client_socket):
        threading.Thread.__init__(self)
        self.connection = client_socket
        self.address = address
        print("connection established with: ", address)

    def run(self):
        account = None
        curr_repo = None
        run = True
        while run:
            rec_message = ""
            message_size = self.connection.recv(2048).decode()
            for _ in range(math.ceil(int(message_size) / 2048)):
                message_part = self.connection.recv(2048).decode()
                if not message_part:
                    run = False
                    break
                rec_message = rec_message + str(message_part)

            cmd, res = server_parser.parse_message(rec_message, account, curr_repo)
            if res is None:
                res = "Fatal error!"
            if cmd == "signUp" or cmd == 'login':
                if type(res) is not str:
                    account = res
                    res = 'Login successful'
            if cmd == 'goto':
                if res is not None:
                    curr_repo = res
                    res = "{} repo is pinned".format(res)
                else:
                    res = 'Wrong repo name!'

            self.connection.sendall(str(len(res.encode('utf-8'))).encode('ascii'))
            self.connection.sendall(bytes(res, 'UTF-8'))
        self.connection.close()
        print(self.address, " disconnected.")


if __name__ == '__main__':
    server = Server(8000, "127.0.0.1")
    server.run()
