class NonRegistered():
    list_of_fields = ['name']

class Registered():
    list_of_fields = ['name', 'favorite']
    email = None

class UserOwner(Registered):
    list_of_fields = ['email', 'password', 'name', 'favorite']

class Admin(UserOwner):
    list_of_fields = None
