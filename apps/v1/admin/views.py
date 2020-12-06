from flask.views import MethodView
from .marshmallows import *
from flask import request, abort
from common.models import Admin
from common.system.login_require import admin_login_required
from sqlalchemy import or_


class AdminLoginView(MethodView):
    """管理员登陆"""
    def post(self):
        req_val = AdminLoginParse().load(request.values)

        result = Admin.login(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])

        return {"code": 200, "token": result['user'].create_token()}


class AdminLogoutView(MethodView):
    """管理退出登录"""
    decorators = [admin_login_required]

    def get(self):
        request.current_user.logout()
        return {"code": 200, "msg": "注销成功"}


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

        query_args = [Admin.is_delete == 0]
        if "word" in req_val.keys():
            query_args.append(or_(
                Admin.nickname.like("%" + req_val['word'] + "%"),
                Admin.username.like("%" + req_val['word'] + "%")
            ))
        admins = Admin.query.filter(*query_args).paginate(req_val['page'], req_val['rows'])

        page_data = PaginateSchema().dump(admins)
        return {"code": 200, "data": AdminListSchema().dump(admins.items), "page_data": page_data}


class AdminInfoView(MethodView):
    """管理员获取、修改、删除"""
    decorators = [admin_login_required]

    def get(self, admin_id):
        admin = Admin.query.filter_by(id=admin_id, is_delete=0).first()
        if not admin:
            abort(404, description="没有找到该管理员")
        return {"code": 200, "data": AdminInfoSchema().dump(admin)}

    def put(self, admin_id):
        req_val = UpdateAdminInfoParse().load(request.values)

        admin = Admin.query.filter_by(id=admin_id, is_delete=0).first()
        if not admin:
            abort(404, description="没有找到该管理员")
        result = admin.update(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])

        return {"code": 200, "msg": "修改成功"}

    def delete(self, admin_id):
        admin = Admin.query.filter_by(id=admin_id, is_delete=0).first()
        if not admin:
            abort(404, description="没有找到该管理员")
        admin.delete()
        return {"code": 200, "msg": "删除成功"}


class AddAdminView(MethodView):
    """创建管理员"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddAdminParse().load(request.values)

        result = Admin.add(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "msg": "添加成功"}




