class Account:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__repositories = dict()  # {repository_name: owner_name}

    def get_username(self):
        return self.__username

    def check_password(self, password):
        return self.__password == password

    def get_password(self):
        return self.__password

    def __eq__(self, other):
        return self.__username == other.get_username()

    def add_repository(self, repository_name, self_owner=True, owner_user=None):
        if self_owner:
            self.__repositories[repository_name] = self
        else:
            self.__repositories[repository_name] = owner_user

    def get_repositories(self):
        return self.__repositories
