class NonRegistered():
    list_of_data = ['name']

class Registered():
    list_of_data = ['name', 'favorite']
    
class UserOwner():
    list_of_data = None
    def change_username(new_username):
        pass

    def change_password(new_password):
        pass

    def change_name(new_name):
        pass

    def change_favorite(new_favorite):
        pass

class Admin(UserOwner):
    list_of_data = None
    def set_admin_role():
        pass
