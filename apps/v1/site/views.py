from flask.views import MethodView
from common.system.login_require import admin_login_required
from .marshmallows import *
from flask import request, abort
from common.models import SiteInfo, db, SocialContact, Navigation, NavigationUrl, Focusing


# 前台接口
class GetSiteInfoView(MethodView):
    """前台获取网站信息"""
    def get(self):
        site = SiteInfo.query.filter_by(id=1).first()
        return {"code": 200, "data": GetSiteInfoSchema().dump(site)}


class GetSocialContactView(MethodView):
    """前台获取社交方式"""
    def get(self):
        contacts = SocialContact.query.filter(SocialContact.is_delete == 0).order_by(SocialContact.sort.asc()).all()
        return {"code": 200, "data": SocialContactListSchema().dump(contacts)}


class GetNavigationView(MethodView):
    """前台获取导航"""
    def get(self):
        navigations = Navigation.query.filter(Navigation.is_delete == 0).order_by(Navigation.sort.asc()).all()
        return {"code": 200, "data": FrontNavigationListSchema().dump(navigations)}


class GetFocusingListView(MethodView):
    """获取聚焦列表"""
    def get(self):
        focus = Focusing.query.filter(Focusing.is_delete == 0).order_by(Focusing.sort.asc()).limit(3).all()
        return {"code": 200, "data": FocusingListSchema().dump(focus)}


# 后台接口
class SiteInfoView(MethodView):
    """获取、修改网站信息"""
    decorators = [admin_login_required]

    def get(self):
        site = SiteInfo.query.filter_by(id=1).first()
        return {"code": 200, "data": SiteInfoSchema().dump(site)}

    def put(self):
        req_val = SiteInfoParse().load(request.values)
        site = SiteInfo.query.filter_by(id=1).first()
        if not site:
            site = SiteInfo(**req_val)
            db.session.add(site)
        else:
            site.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}


class AddSocialContactView(MethodView):
    """添加社交方式"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddSocialContactParse().load(request.values)

        contact = SocialContact(**req_val)
        db.session.add(contact)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class SocialContactView(MethodView):
    """获取、修改、删除社交方式"""
    decorators = [admin_login_required]

    def get(self, contact_id):
        contact = SocialContact.query.filter(SocialContact.id == contact_id, SocialContact.is_delete == 0).first()
        if not contact:
            abort(404, description="这个社交方式不存在")
        return {"code": 200, "data": GetSocialContactSchema().dump(contact)}

    def put(self, contact_id):
        req_val = UpdateSocialContactParse().load(request.values)
        contact = SocialContact.query.filter(SocialContact.id == contact_id, SocialContact.is_delete == 0).first()
        if not contact:
            abort(404, description="这个社交方式不存在")

        contact.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, contact_id):
        contact = SocialContact.query.filter(SocialContact.id == contact_id, SocialContact.is_delete == 0).first()
        if not contact:
            abort(404, description="这个社交方式不存在")
        contact.delete()
        return {"code": 200, "msg": "删除成功"}


class SocialContactAdminListView(MethodView):
    """获取社交方式列表"""
    decorators = [admin_login_required]

    def get(self):
        contacts = SocialContact.query.filter(SocialContact.is_delete == 0).order_by(SocialContact.sort.asc()).all()
        return {"code": 200, "data": SocialContactAdminListSchema().dump(contacts)}


class AddNavigationView(MethodView):
    """添加导航"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddNavigationParse().load(request.values)

        navigation = Navigation(**req_val)
        db.session.add(navigation)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class NavigationInfoView(MethodView):
    """获取、修改、删除导航数据"""
    decorators = [admin_login_required]

    def get(self, navigation_id):
        navigation = Navigation.query.filter(Navigation.id == navigation_id, Navigation.is_delete == 0).first()
        if not navigation:
            abort(400, description="没有找到该导航")
        return {"code": 200, "data": NavigationInfoSchema().dump(navigation)}

    def put(self, navigation_id):
        req_val = UpdateNavigationInfoParse().load(request.values)
        navigation = Navigation.query.filter(Navigation.id == navigation_id, Navigation.is_delete == 0).first()
        if not navigation:
            abort(400, description="没有找到该导航")

        navigation.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, navigation_id):
        navigation = Navigation.query.filter(Navigation.id == navigation_id, Navigation.is_delete == 0).first()
        if not navigation:
            abort(400, description="没有找到该导航")

        navigation.delete()
        return {"code": 200, "msg": "删除成功"}


class NavigationAdminListView(MethodView):
    """获取导航列表"""
    decorators = [admin_login_required]

    def get(self):
        navigations = Navigation.query.filter(Navigation.is_delete == 0).order_by(Navigation.sort.asc()).all()
        return {"code": 200, "data": NavigationAdminListSchema().dump(navigations)}


class NavigationUrlView(MethodView):
    """修改、删除导航链接"""
    decorators = [admin_login_required]

    def put(self, navigation_url_id):
        req_val = UpdateNavigationUrlParse().load(request.values)
        link = NavigationUrl.query.filter(NavigationUrl.id == navigation_url_id, NavigationUrl.is_delete == 0).first()
        if not link:
            abort(400, description="没有找到该导航链接")
        link.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, navigation_url_id):
        link = NavigationUrl.query.filter(NavigationUrl.id == navigation_url_id, NavigationUrl.is_delete == 0).first()
        if not link:
            abort(400, description="没有找到该导航链接")
        link.delete()
        return {"code": 200, "msg": "删除成功"}


class AddNavigationUrlView(MethodView):
    """添加导航链接"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddNavigationUrlParse().load(request.values)
        link = NavigationUrl(**req_val)
        db.session.add(link)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class AddFocusingView(MethodView):
    """添加聚焦"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddFocusingParse().load(request.values)
        model = Category.MODULE_TYPE[req_val['module']]
        focus = model.query.filter(model.is_delete == 0, model.id == req_val['focus_id']).first()
        if not focus:
            abort(404, description="聚焦内容不存在")

        db.session.add(Focusing(**req_val))
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class FocusingListAdminView(MethodView):
    """获取聚焦列表"""
    decorators = [admin_login_required]

    def get(self):
        focus = Focusing.query.filter(Focusing.is_delete == 0).order_by(Focusing.sort.asc()).all()
        return {"code": 200, "data": FocusingListAdminSchema().dump(focus)}


class FocusingInfoView(MethodView):
    """修改、删除"""
    decorators = [admin_login_required]

    def put(self, focus_id):
        req_val = UpdateFocusingInfoParse().load(request.values)
        model = Category.MODULE_TYPE[req_val['module']]
        focus_obj = model.query.filter(model.is_delete == 0, model.id == req_val['focus_id']).first()
        if not focus_obj:
            abort(404, description="聚焦内容不存在")
        focus = Focusing.query.filter_by(id=focus_id, is_delete=0).first()
        if not focus:
            abort(404, description="该聚焦不存在")

        focus.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, focus_id):
        focus = Focusing.query.filter_by(id=focus_id, is_delete=0).first()
        if not focus:
            abort(404, description="该聚焦不存在")
        focus.delete()
        return {"code": 200, "msg": "删除成功"}



