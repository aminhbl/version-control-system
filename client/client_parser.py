from server.git_manager import pull_client_side


def printHelp():
    helpStr = "-help:  To show the help list\n\n"
    helpStr = helpStr + "push:   push –m “commit message” –f “./dir/file”"
    print(helpStr)


def parseInput(command):

    messageToSend = ""
    command = str(command)
    if command.startswith("-help"):
        printHelp()
        return ""

    if command.startswith("signup"):
        name = input("Enter your name: ")
        password1 = input("Enter you password: ")
        password2 = input("Renter you password: ")
        if password1 == password2:
            messageToSend = messageToSend + "1$"
            messageToSend = messageToSend + name + "$"
            messageToSend = messageToSend + password1 + "$"
        else:
            print("Password doesn't match\n\n")

    if command.startswith("signin"):
        name = input("Enter your Username: ")
        password = input("Enter you password: ")
        messageToSend = messageToSend + "2$"
        messageToSend = messageToSend + name + "$"
        messageToSend = messageToSend + password + "$"

    if command.startswith("mkrepo"):
        parts = command.split()
        messageToSend = messageToSend + "3$"
        messageToSend = messageToSend + parts[1] + "$"

    if command.startswith("list"):
        messageToSend = messageToSend + "4$"

    if command.startswith("choose"):
        parts = command.split()
        messageToSend = messageToSend + "5$"
        messageToSend = messageToSend + parts[1] + "$"

    if command.startswith("push"):
        parts = command.split()
        commitMessage = command.split("\"")[1]
        data = pull_client_side(parts[-1][1:-1], parts[-2][1])
        messageToSend = messageToSend + "6$"
        messageToSend = messageToSend + commitMessage + "$"
        messageToSend = messageToSend + data + "$"

    if command.startswith("pull"):
        parts = command.split()
        messageToSend = messageToSend + "7$"
        messageToSend = messageToSend + parts[-2][1] + "$"
        messageToSend = messageToSend + parts[2][1:-1] + "$"

    if command.startswith("view"):
        messageToSend = "8$"

    if command.startswith("sync"):
        messageToSend = messageToSend + "9$"

    if command.startswith("userslist"):
        messageToSend = messageToSend + "10$"

    if command.startswith("cont"):
        parts = command.split()
        messageToSend = messageToSend + "11$"
        messageToSend = messageToSend + parts[1] + "$"

    if command.startswith("repolsof"):
        parts = command.split()
        messageToSend = messageToSend + "12$"
        messageToSend = messageToSend + parts[1] + "$"

    if command.startswith("Opull"):
        parts = command.split()
        messageToSend = messageToSend + "13$"
        messageToSend = messageToSend + parts[1] + "$"
        messageToSend = messageToSend + parts[2] + "$"
        messageToSend = messageToSend + parts[3][1] + "$"
        messageToSend = messageToSend + parts[4][1:-1] + "$"

    return messageToSend


