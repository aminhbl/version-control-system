import os
import pickle
import file_handler
from account import *


def authenticate_user(username, password):
    users = load_users()

    for user in users:
        if user.get_username() == username and user.check_password(password):
            return user

    return None


def load_users():
    file = None
    try:
        file = open('./data/users.raw', 'rb')
        users = pickle.load(file)
    except IOError as er:
        users = list()
    finally:
        if file is not None:
            file.close()

    return users


def save_users(users):
    file = None
    try:
        file = open('./data/users.raw', 'wb')
        pickle.dump(users, file)
    except IOError as error:
        print(error)
    finally:
        file.close()


def allocate_new_user(username, password):
    users = load_users()

    new_user = Account(username, password)

    for user in users:
        if new_user == user:
            return False

    users.append(new_user)

    save_users(users)

    base_directory = new_user.get_username()
    path = os.path.join('./data', base_directory)

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    return True


def pull_server_side(username, password, repository, path, type_):
    user = authenticate_user(username, password)
    if user is None:
        return None
    pathT = path

    last = os.getcwd()
    os.chdir("data/" + user.get_username() + "/" + repository)
    ans = file_handler.encoder(type_, pathT)
    os.chdir(last)

    return ans


def push_server_side(username, password, messageBody, repository, commit_message):
    user = authenticate_user(username, password)
    if user is None:
        return None
    pathT = "data/" + user.get_username() + "/" + repository
    print(pathT)
    file_handler.decoder(messageBody, pathT, commit_message)


def pull_client_side(path, type_):
    return file_handler.encoder(type_, path)


def push_client_side(messageBody, path):
    file_handler.decoder(messageBody, path)


def create_repository_for_user(username, password, repository_name):
    user = authenticate_user(username, password)
    users = load_users()
    if user is None:
        return False
    base_directory = user.get_username()
    path = os.path.join('./data', base_directory, repository_name)

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
    for user_ in users:
        if user_ == user:
            user_.add_repository(repository_name)
            break

    save_users(users)

    return True

