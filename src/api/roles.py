class NonRegistered():
    list_of_fields = ['name']

class Registered():
    list_of_fields = ['name', 'favorite']
    email = None

class UserOwner(Registered):
    list_of_fields = ['email', 'password', 'name', 'favorite']
    def change_email(new_email):
        pass

    def change_password(new_password):
        pass

    def change_name(new_name):
        pass

    def change_favorite(new_favorite):
        pass

class Admin(UserOwner):
    list_of_fields = None
    def set_admin_role():
        pass
