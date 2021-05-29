import coding
from server.git_manager import client_push


def build_message(cmd):
    cmd = str(cmd)
    parts = cmd.split()

    if "signUp" in cmd:
        name = input("username: ")
        password = input("password: ")
        return "#".join(["signUp", name, password, "#"])

    if "login" in cmd:
        name = input("username: ")
        password = input("password: ")
        return "#".join(["login", name, password, "#"])

    if "origin" in cmd:
        if len(parts) < 2:
            print('Repo name not specified!')
            return None
        else:
            return "#".join(["origin", parts[1], "#"])

    if "lsRepo" in cmd:
        if len(parts) > 1:
            return "#".join(["rlsRepo", parts[1], "#"])
        return "lsRepo#"

    if "lsDir" in cmd:
        if len(parts) < 2:
            print('Repo name not specified!')
            return None
        else:
            return "#".join(["lsDir", parts[1], "#"])

    if "download" in cmd:
        return "sync#"

    if "pin" in cmd:
        if len(parts) < 2:
            print('Repo name not specified!')
            return None
        else:
            return "#".join(["goto", parts[1], "#"])

    if "push" in cmd:
        path = parts[-1].split("\"")[1]
        commitMessage = cmd.split("\"")[1]
        pattern = parts[-2][1]
        # push to be placed on server:
        data = client_push(path, pattern)
        return "#".join(["push", commitMessage, data, "#"])

    if "pull" in cmd:
        return "#".join(["pull", parts[-2][1], parts[2][1:-1], "#"])

    if "dlRepo" in cmd:
        return "#".join(["+Pull", parts[1], parts[2], "-d", "./", "#"])

    if "lsComm" in cmd:
        return "lsComm#"

    if "sync" in cmd:
        return "sync#"

    if "allAccounts" in cmd:
        return "allAccounts#"

    if "invCollab" in cmd:
        if len(parts) < 2:
            print('Collaborator name not specified!')
            return None
        return "#".join(["invCollab", parts[1], "#"])

    if "+Pull" in cmd:
        return "#".join(["+Pull", parts[1], parts[2], parts[3][1], parts[4][1:-1], "#"])

    if cmd.startswith('cd'):
        return "cd" + parts[1]

    print('Wrong input!')
    return None
