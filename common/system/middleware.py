from flask import request
from common.models import User
from common.system.errors import invalid_token


def middleware_register(app):

    @app.before_request
    def identity_check():
        # token校验
        token = request.headers.get('Authorization', None)
        request.current_user = None
        if token:
            user = User.check_token(token)
            if user['status'] == "success":
                request.current_user = user['user']
            else:
                return invalid_token()
        return None

