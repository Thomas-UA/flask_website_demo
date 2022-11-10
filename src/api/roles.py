class NonRegistered():
    list_of_fields = ['username']

class Registered():
    username = None

    list_of_fields = ['username', 'favorite']
    
    def __init__(self, username):
        self.username = username

    def is_user_owner(self, query_username):
        if self.username == query_username:
            self.list_of_fields = None

        return self.list_of_fields

class Admin():
    list_of_fields = None
