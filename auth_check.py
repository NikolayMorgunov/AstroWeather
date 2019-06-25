from users_db import *


def auth_check(username, password):
    user_in_db = User.select().where(User.username == username and User.password == password)
    if user_in_db:
        return True
    return False
