from git_manager import *


def parseReceivedMessage(command, user, current_repository):
    parts = command.split("$")
    action = parts[0]
    print("action: ", action)
    if action == '1' and user is None:
        ans = allocate_new_user(parts[1], parts[2])
        # user = authenticate_user(parts[1], parts[2])
        if not ans:
            return "User exists"
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
            with open("DB/" + user.get_username() + "/" + current_repository + "/commits.txt", "r") as o:
                return o.read()
        except FileExistsError:
            print("Commit file not found!")

    if action == '9' and user is not None:
        if current_repository is None:
            return "First choose a repository"
        body = pull_server_side(user.get_username(), user.get_password(), current_repository, "./", "-d")
        return "pull_request" + str(body)

    if action == '10':
        users = load_users()
        print(type(users))
        ans = ""
        for i in users:
            ans = ans + "\n" + i.get_username()
        return ans

    if action == '11' and user is not None:
        if current_repository is None:
            return "First choose a repository"
        add_contributor(user.get_username(), user.get_password(), parts[1], current_repository)
        return "Added successfully"

    if action == '12' and user is not None:
        users = load_users()
        for user_ in users:
            if user_.get_username() == parts[1]:
                repositories = user_.get_repositories()
                answer = ""
                for x in repositories:
                    answer = answer + "\n" + str(x)
                return answer

    if action == '13' and user is not None:
        body = Opull_server_side(parts[1], parts[2], parts[4], parts[3])
        return "pull_request" + str(body)
