import os
import coding
from datetime import *
import file_handler
from server.account import Account


def authenticate_account(username, password):
    accounts = restore_accounts()
    for account in accounts:
        if account.authenticate(username, password):
            return account
    return None


def restore_accounts():
    accounts = file_handler.pickle_read('server/DB/accounts')
    if accounts is None:
        return list()
    return accounts


def store_accounts(users):
    file_handler.pickle_write('server/DB/accounts', users)


def create_account(username, password):
    accounts = restore_accounts()
    new_acc = Account(username, password)
    for account in accounts:
        if new_acc.get_username() == account.get_username():
            return False
    accounts.append(new_acc)
    store_accounts(accounts)
    try:
        account_root = os.path.join('server/DB', new_acc.get_username())
        os.mkdir(account_root)
    except OSError as error:
        print(error)
    return True


def fetch_plus(username, repository, path, pattern):
    before = os.getcwd()
    os.chdir("server/DB/" + username + "/" + repository)
    res = coding.encode(pattern, path)
    os.chdir(before)
    return res


def register_commit(root, commit_message, username):
    if commit_message is not None:
        data = "${} @ {} : {}\n".format(username, datetime.now(), commit_message)
        file_handler.write_text(root + "/" + "commits.txt", data)


def place_on_server(username, password, messageBody, repository, commit_message):
    account = authenticate_account(username, password)
    repositories = account.get_repositories()
    for rep in repositories:
        if rep == repository:
            path = "server/DB/" + repositories[rep].get_username() + "/" + repository
            coding.decode(messageBody, path)
            register_commit(path, commit_message, username)
            break


def client_push(path, type_):
    return coding.encode(type_, path)


def fetch_from_server(username, password, repository, path, pattern):
    account = authenticate_account(username, password)
    repositories = account.get_repositories()
    for rep in repositories:
        if rep == repository:
            before = os.getcwd()
            os.chdir("server/DB/" + repositories[rep].get_username() + "/" + repository)
            res = coding.encode(pattern, path)
            os.chdir(before)
            return res


def add_contributor(username, password, new_user_username, repository):
    account = authenticate_account(username, password)
    accounts = restore_accounts()
    for acc in accounts:
        if acc.get_username() == new_user_username:
            acc.add_repository(repository, self_owner=False, owner_user=account)
            store_accounts(accounts)


def create_repo(username, password, repository_name):
    accounts = restore_accounts()
    curr_account = authenticate_account(username, password)
    path = os.path.join('server/DB', username, repository_name)
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
    for acc in accounts:
        if acc.get_username() == curr_account.get_username():
            acc.add_repository(repository_name)
            break
    store_accounts(accounts)
