

class Account:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__repositories = dict()

    def get_username(self):
        return self.__username

    def check_password(self, password):
        return self.__password == password

    def get_password(self):
        return self.__password

    def __eq__(self, other):
        return self.__username == other.get_username()

    def add_repository(self, repository_name):
        self.__repositories[repository_name] = set().add(self.__username)

    def get_repositories(self):
        return self.__repositories
