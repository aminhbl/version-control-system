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


def place_on_server(username, password, messageBody, repository, commit_message):
    # change something
    account = authenticate_account(username, password)
    repositories = account.get_repositories()
    owner = ""
    for rep in repositories:
        if rep == repository:
            owner = repositories[rep]
            break
    pathT = "server/DB/" + owner.get_username() + "/" + repository
    coding.decode(messageBody, pathT)
    register_commit(pathT, commit_message)


def register_commit(root, commit_message):
    if commit_message is not None:
        file_handler.write_text(root + "/" + "commits.txt", "{}|{}\n".format(commit_message, datetime.now()))


def pull_client_side(path, type_):
    return coding.encode(type_, path)


def fetch_from_server(username, password, repository, path, pattern):
    account = authenticate_account(username, password)
    repositories = account.get_repositories()
    repo_owner = None
    for rep in repositories:
        if rep == repository:
            repo_owner = repositories[rep]
            break
    before = os.getcwd()
    os.chdir("server/DB/" + repo_owner.get_username() + "/" + repository)
    res = coding.encode(pattern, path)
    os.chdir(before)
    return res


def add_contributor(username, password, new_user_username, repository):
    user = authenticate_account(username, password)
    users = restore_accounts()
    for user_ in users:
        if user_.get_username() == new_user_username:
            user_.add_repository(repository, self_owner=False, owner_user=user)
            store_accounts(users)


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
