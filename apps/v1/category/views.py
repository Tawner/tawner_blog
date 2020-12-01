from flask.views import MethodView
from common.system.login_require import admin_login_required
from .marshmallows import *
from flask import request, abort


# 前台接口
class CategoryListView(MethodView):
    """栏目列表"""
    def get(self):
        category = Category.query.filter(
            Category.is_delete == 0,
            Category.level == 1
        ).order_by(Category.sort.asc()).all()
        return {"code": 200, "data": CategoryListSchema().dump(category)}


# 后台接口
class AddCategoryView(MethodView):
    decorators = [admin_login_required]
    """添加栏目"""
    def post(self):
        req_val = AddCategoryParse().load(request.values)
        Category.add(**req_val)
        return {"code": 200, "msg": "添加成功"}


class CategoryView(MethodView):
    decorators = [admin_login_required]
    """栏目获取、修改、删除"""
    def get(self, category_id):
        category = Category.query.filter(Category.id == category_id, Category.is_delete == 0).first()
        if not category:
            abort(404, description="该栏目不存在")
        return {"code": 200, "data": CategoryInfoSchema().dump(category)}

    def put(self, category_id):
        req_val = UpdateCategoryParse().load(request.values)
        category = Category.query.filter(Category.id == category_id, Category.is_delete == 0).first()
        if not category:
            abort(404, description="该栏目不存在")
        result = category.update(**req_val)
        if result['stauts'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "msg": "修改成功"}

    def delete(self, category_id):
        category = Category.query.filter(Category.id == category_id, Category.is_delete == 0).first()
        if not category:
            abort(404, description="该栏目不存在")
        if not category.empty():
            abort(400, description="该栏目下有内容或子栏目无法删除")
        category.delete()
        return {"code": 200, "msg": "删除成功"}


class CategoryListAdminView(MethodView):
    decorators = [admin_login_required]
    """获取栏目列表"""
    def get(self):
        req_val = CategoryListAdminParse().load(request.values)

        query_args = [ Category.is_delete == 0, Category.level == 1]
        if req_val.get('module', None):
            query_args.append(Category.module == req_val['module'])
        category = Category.query.filter(*query_args).order_by(Category.sort.asc()).all()
        return {"code": 200, "data": CategoryListAdminSchema().dump(category)}

