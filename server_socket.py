import math
import socket
import threading
from copy import deepcopy
from git_manager import *

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
            # print("from client at {}: {}".format(self.address[1], data_size))
            if username is not None:
                answer = parseReceivedMessage(string_data, authenticate_user(username, password), current_repository)
            else:
                answer = parseReceivedMessage(string_data, None, current_repository)

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


def parseReceivedMessage(command, user, current_repository):
    parts = command.split("$")
    action = parts[0]
    print("action: ", action)
    if action == '1' and user is None:
        allocate_new_user(parts[1], parts[2])
        user = authenticate_user(parts[1], parts[2])
        return "User created"

    if action == '2' and user is None:
        user = authenticate_user(parts[1], parts[2])
        if user is None:
            return None
        return [user.get_username(), user.get_password()]

    if action == '3' and user is not None:
        create_repository_for_user(user.get_username(), user.get_password(), parts[1])
        return "done"

    if action == '4' and user is not None:
        repositories = user.get_repositories()
        answer = ""
        for x in repositories:
            answer = answer + "\n" + str(x)
        return answer

    if action == '5' and user is not None:
        if current_repository is not None:
            return "Your are currently in a repository!!!"
        repository_name = parts[1]
        repositories = user.get_repositories()
        exist = False
        for x in repositories:
            if str(x) == str(repository_name):
                exist = True
                break
        if not exist:
            return None
        return [repository_name]

    if action == '6' and user is not None:
        if current_repository is None:
            return "First choose a repository"
        push_server_side(user.get_username(), user.get_password(), parts[2], current_repository, parts[1])
        return "Pushed successfully"

    if action == '7' and user is not None:
        if current_repository is None:
            return "First choose a repository"
        body = pull_server_side(user.get_username(), user.get_password(), current_repository, parts[2], parts[1])
        return "pull_request" + str(body)

    if action == '8' and user is not None:
        if current_repository is None:
            return "First choose a repository"
        try:
            with open("data/" + user.get_username() + "/" + current_repository + "/commits.txt", "r") as o:
                return o.read()
        except FileExistsError:
            print("Commit file not found!")


if __name__ == '__main__':
    server()
