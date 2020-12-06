from flask import request
from common.models import User, Admin
from common.utility import decrypt
from flask import abort


def middleware_register(app):

    @app.before_request
    def identity_check():
        # token校验
        token = request.headers.get('Authorization', None)
        request.current_user = None
        if token:
            token_data = decrypt(token)
            if token_data:
                user_model_dict = {"admin": Admin, "user": User}
                user_model = user_model_dict[token_data['type']]
                result = user_model.check_token(token_data['id'], token)
                if result['status'] == "success":
                    request.current_user = result['user']
                else:
                    return abort(401, description="token有误")
            else:
                return abort(401, description="token有误")
        return None

