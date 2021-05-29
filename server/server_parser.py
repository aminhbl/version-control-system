from git_manager import *
import file_handler
from account import *


def parse_message(message, account, curr_repo):
    split_message = message.split("#")
    cmd = split_message[0]
    print("cmd: ", cmd)
    curr_username = None
    curr_pass = None
    repositories = None
    if account is not None:
        account = authenticate_account(account.get_username(), account.get_password())
        curr_username = account.get_username()
        curr_pass = account.get_password()
        repositories = account.get_repositories()

    if cmd == 'signUp':
        res = create_account(split_message[1], split_message[2])
        if not res:
            return cmd, "Choose another username!"
        account = authenticate_account(split_message[1], split_message[2])
        return cmd, account

    if cmd == 'login':
        account = authenticate_account(split_message[1], split_message[2])
        if account is None:
            return cmd, 'Login failed!'
        else:
            return cmd, account

    if cmd == 'origin':
        res = create_repo(curr_username, curr_pass, split_message[1])
        print(res)
        return cmd, "Repo created."

    if cmd == 'lsRepo':
        repo_list = list(repositories.keys())
        repos = '{}\'s repos:\n'.format(curr_username)
        repos += "\n".join(repo_list)
        if repos == '{}\'s repos:\n'.format(curr_username):
            repos = "No repo yet!"
        return cmd, repos

    if cmd == 'goto':
        repository_name = split_message[1]
        for repo in repositories:
            if str(repo) == str(repository_name):
                return cmd, repository_name
        return cmd, None

    if cmd == 'allAccounts':
        accounts = list(map(Account.get_username, load_accounts()))
        accounts_list = 'All the accounts:\n'
        accounts_list += "\n".join(accounts)
        return cmd, accounts_list

    if cmd == 'rlsRepo':
        accounts = load_accounts()
        for u in accounts:
            if u.get_username() == split_message[1]:
                print(u.get_repositories())
                repositories = list(u.get_repositories().keys())
                repos = '{}\'s repos:\n'.format(u.get_username())
                repos += '\n'.join(repositories)
                return cmd, repos
        return cmd, "Account not found!"

    if cmd == '+Pull':
        return cmd, "pull#" + str(Opull_server_side(split_message[1], split_message[2], split_message[4],
                                                    split_message[3]))

    if curr_repo is not None:
        if cmd == 'push':
            push_server_side(curr_username, curr_pass, split_message[2], curr_repo, split_message[1])
            return cmd, "Push successful"

        if cmd == 'pull':
            return cmd, "pull#" + str(pull_server_side(curr_username, curr_pass, curr_repo, split_message[2],
                                                       split_message[1]))

        if cmd == 'lsComm':
            commit_path = "server/DB/" + curr_username + "/" + curr_repo + "/commits.txt"
            return cmd, 'Current repo\'s commits:\n' + file_handler.read_text(commit_path)

        if cmd == 'sync':
            return cmd, "pull#" + str(pull_server_side(curr_username, curr_pass, curr_repo, "./", "-d"))

        if cmd == 'invCollab':
            if split_message[1] is None:
                return cmd, 'User not specified!'
            add_contributor(curr_username, curr_pass, split_message[1], curr_repo)
            return cmd, "{} added as new collaborator".format(split_message[1])
    else:
        return cmd, "Choose a repo first!"
