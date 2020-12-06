from flask.views import MethodView
from common.system.login_require import admin_login_required, user_login_required
from .marshmallows import *
from flask import request, abort, current_app
from common.models import User, db
from common.email.email import send_email
from threading import Thread
from common.utility import random_str
from common.redis.redis import Redis
from sqlalchemy import or_


# 前台接口
class UserLoginView(MethodView):
    """前台登录接口"""

    def post(self):
        req_val = UserLoginParse().load(request.values)
        result = User.login(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "token": result['user'].create_token()}


class UserLogoutView(MethodView):
    """前台退出登录接口"""
    decorators = [user_login_required]

    def get(self):
        request.current_user.logout()
        return {"code": 200, "msg": "注销成功"}


class UserRegisterView(MethodView):
    """前台注册接口"""

    def post(self):
        req_val = UserRegisterParse().load(request.values)

        result = User.register(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "msg": "注册成功"}


class SendEmailCodeView(MethodView):
    """发送验证啊接口"""

    def post(self):
        req_val = SendEmailCodeParse().load(request.values)

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


class TokenUserInfoView(MethodView):
    """token获取、修改用户信息"""
    decorators = [user_login_required]

    def get(self):
        return {"code": 200, "data": TokenUserInfoSchema().dump(request.current_user)}

    def put(self):
        req_val = UpdateUserInfoParse().load(request.values)
        request.current_user.update(**req_val)
        return {"code": 200, "msg": "修改成功"}


class UserModifyPasswordView(MethodView):
    """token修改密码"""
    decorators = [user_login_required]

    def put(self):
        req_val = UserModifyPasswordParse().load(request.values)
        result = request.current_user.modify_password(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "msg": "修改成功"}


# 后台接口
class UserListView(MethodView):
    """用户列表"""
    decorators = [admin_login_required]

    def get(self):
        req_val = UserListParse().load(request.values)

        query_args = [User.is_delete == 0]
        if "word" in req_val.keys():
            query_args.append(or_(
                User.nickname.like("%" + req_val['word'] + "%"),
                User.email.like("%" + req_val['word'] + "%")
            ))
        users = User.query.filter(*query_args).order_by(User.id.desc()).paginate(req_val['page'], req_val['rows'])
        page_data = PaginateSchema().dump(users)
        return {"code": 200, "page_data": page_data, "data": UserListSchema().dump(users.items)}


class DeleteUserView(MethodView):
    """删除用户"""
    decorators = [admin_login_required]

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id, is_delete=0).first()
        if not user:
            abort(400, description="该用户不存在")
        user.delete()
        return {"code": 200, "msg": "删除成功"}




