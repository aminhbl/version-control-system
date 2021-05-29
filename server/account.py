class Account:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__repositories = dict()

    def get_username(self):
        return self.__username

    def authenticate(self, username, password):
        return self.__username == username and self.__password == password

    def get_password(self):
        return self.__password

    def add_repository(self, repository_name, self_owner=True, owner_user=None):
        if self_owner:
            self.__repositories[repository_name] = self
        else:
            self.__repositories[repository_name] = owner_user

    def get_repositories(self):
        return self.__repositories
