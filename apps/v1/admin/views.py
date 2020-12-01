from flask.views import MethodView
from .marshmallows import *
from flask import request, abort
from common.models import *
from common.system.login_require import admin_login_required
from sqlalchemy import or_


class AdminLoginView(MethodView):
    """管理员登陆"""
    def post(self):
        req_val = AdminLoginParse().load(request.values)

        result = User.check_password(req_val['username'], req_val['password'])
        if result['status'] == "failure":
            abort(400, description=result['msg'])
        if not result['user'].is_super:
            abort(400, description="用户名不存在")

        return {"code": 200, "token": result['user'].create_token()}


class TokenAdminInfoView(MethodView):
    """token获取管路员信息"""
    decorators = [admin_login_required]

    def get(self):
        return {"code": 200, "data": AdminInfoSchema().dump(request.current_user)}


class GetAdminListView(MethodView):
    """获取管理员列表"""
    decorators = [admin_login_required]

    def get(self):
        req_val = GetAdminListParse().load(request.values)

        query_args = [User.is_delete == 0, User.is_super == 1]
        if "word" in req_val.keys():
            query_args.append(or_(
                User.nickname.like("%" + req_val['word'] + "%"),
                User.username.like("%" + req_val['word'] + "%")
            ))
        admins = User.qeury.filter(*query_args).paginate(req_val['page'], req_val['rows'])

        page_data = PaginateSchema(admins)
        return {"code": 200, "data": AdminListSchema().dump(admins.items), "page_data": page_data}


class AdminInfoView(MethodView):
    """管理员获取、修改、删除"""
    decorators = [admin_login_required]

    def get(self, admin_id):
        admin = User.qeury.filter(User.id == admin_id, User.is_super == 1, User.is_delete == 0).first()
        if not admin:
            abort(404, description="没有找到该管理员")
        return {"code": 200, "data": AdminInfoSchema().load(admin)}

    def put(self, admin_id):
        req_val = UpdateAdminInfoParse().load(request.values)

        if req_val.get("password", None) != req_val.pop("password_", None):
            abort(400, description="两次密码不一致")

        admin = User.qeury.filter(User.id == admin_id, User.is_super == 1, User.is_delete == 0).first()
        if not admin:
            abort(404, description="没有找到该管理员")
        admin.update(**req_val)
        return {"code": 200, "msg": "修改成功"}

    def delete(self, admin_id):
        admin = User.qeury.filter(User.id == admin_id, User.is_super == 1, User.is_delete == 0).first()
        if not admin:
            abort(404, description="没有找到该管理员")
        admin.delete()
        return {"code": 200, "msg": "删除成功"}


class AddAdminView(MethodView):
    """创建管理员"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddAdminParse().load(request.values)
        if req_val['password'] != req_val.pop('_password'):
            abort(400, description="两次密码不一致")

        result = User.add(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "msg": "添加成功"}




