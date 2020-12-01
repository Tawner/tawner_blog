from flask import request, abort


def admin_login_required(func):
    def wrapper(*args, **kwargs):
        if request.current_user and request.current_user.is_super:
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


def user_login_required(func):
    def wrapper(*args, **kwargs):
        if request.current_user:
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper





