import os
import pickle
import coding
import subprocess
from server.account import Account


def authenticate_user(username, password):
    users = load_users()

    for user in users:
        if user.get_username() == username and user.check_password(password):
            return user

    return None


def load_users():
    file = None
    try:
        file = open('server/DB/accounts', 'rb')
        users = pickle.load(file)
    except IOError:
        users = list()
    finally:
        if file is not None:
            file.close()

    return users


def save_users(users):
    file = None
    try:
        file = open('server/DB/accounts', 'wb')
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
    path = os.path.join('server/DB', base_directory)

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

    repositories = user.get_repositories()
    answer = ""
    for x in repositories:
        if x == repository:
            answer = repositories[x]
            break

    last = os.getcwd()
    print("server/DB/" + answer.get_username() + "/" + repository)
    os.chdir("server/DB/" + answer.get_username() + "/" + repository)
    ans = coding.encode(type_, pathT)
    os.chdir(last)

    print(ans)
    return ans


def Opull_server_side(username, repository, path, type_):
    pathT = path
    last = os.getcwd()
    os.chdir("server/DB/" + username + "/" + repository)
    ans = coding.encode(type_, pathT)
    os.chdir(last)
    return ans


def push_server_side(username, password, messageBody, repository, commit_message):
    user = authenticate_user(username, password)
    if user is None:
        return False
    repositories = user.get_repositories()
    answer = ""
    for x in repositories:
        if x == repository:
            answer = repositories[x]
            break
    pathT = "server/DB/" + answer.get_username() + "/" + repository
    print(pathT)
    coding.decode(messageBody, pathT, commit_message)

    return True


def pull_client_side(path, type_):
    return coding.encode(type_, path)


def push_client_side(messageBody, path):
    coding.decode(messageBody, path)


def add_contributor(username, password, new_user_username, repository):
    user = authenticate_user(username, password)
    users = load_users()
    if user is None:
        return False

    for user_ in users:
        if user_.get_username() == new_user_username:
            user_.add_repository(repository, self_owner=False, owner_user=user)
            save_users(users)
            return True

    return False


def create_repository_for_user(username, password, repository_name):
    user = authenticate_user(username, password)
    users = load_users()
    if user is None:
        return False
    base_directory = user.get_username()
    path = os.path.join('server/DB', base_directory, repository_name)

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
