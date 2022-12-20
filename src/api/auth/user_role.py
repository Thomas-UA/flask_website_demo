class User:
    fields = ["uname", "favorite"]

    def __init__(self, user_token):
        self.user_token = user_token

    def is_user_owner(self, uname):
        return uname == self.user_token


class NotRegistered:
    fields = ["uname"]

    def is_user_owner(self, *args):
        raise NotImplementedError


def user_factory(token=None):
    if token is not None:
        return User(token)

    return NotRegistered
