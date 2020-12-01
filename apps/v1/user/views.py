from flask.views import MethodView
from common.system.login_require import admin_login_required, user_login_required
from .marshmallows import *
from flask import request, abort, current_app, render_template
from common.models import User
from common.email.email import send_email
from threading import Thread
from common.utility import random_str
from common.redis.redis import Redis


# 前台接口
class UserLoginView(MethodView):
    """前台登陆接口"""
    def post(self):
        req_val = UserLoginParse().load(request.values)
        result = User.check_password(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])

        return {"code": 200, "token": result['user'].create_token()}


class UserInfoView(MethodView):
    """token获取、修改用户信息"""
    decorators = [user_login_required]

    def get(self):
        return {"code": 200, "data": UserInfoSchema().load(request.current_user)}

    def put(self):
        req_val = UpdateUserInfoParse().load(request.values)


class EmailValidateView(MethodView):
    """邮箱校验"""
    def post(self):
        req_val = EmailValidateParse().load(request.values)

        param = {
            "app": current_app._get_current_object(),
            "email": req_val['email'],
            "title": "邮箱验证通知",
            "template": "code",
            "code": random_str(2, 6)
        }
        thr = Thread(target=send_email, kwargs=param)
        thr.start()
        redis_obj = Redis()
        redis_obj.write(req_val['email'], param['code'], 300)
        return {"code": 200, "msg": "邮件发送成功"}





