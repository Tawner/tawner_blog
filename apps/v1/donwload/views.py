from flask.views import MethodView
from .marshmallows import *
from flask import request, abort
from common.models import Download, db
from common.system.login_require import admin_login_required


# 前台接口
class DownloadListView(MethodView):
    """获取下载列表"""

    def get(self):
        req_val = DownloadListParse().load(request.values)

        download = Download.list(**req_val)
        page_data = PaginateSchema().dump(download)
        return {"code": 200, "page_data": page_data, "data": DownloadListSchema().dump(download.items)}


class DownloadFileView(MethodView):
    """获取下载链接"""

    def get(self, download_id):
        download = Download.query.filter_by(id=download_id, is_delete=0).first()
        if not download:
            abort(400, description="这个软件不存在")
        return {"code": 200, "url": download.file.url}


# 后台接口
class DownloadListAdminView(MethodView):
    """获取下载列表"""
    decorators = [admin_login_required]

    def get(self):
        req_val = DownloadListAdminParse().load(request.values)
        download = Download.list(**req_val)
        page_data = PaginateSchema().dump(download)
        return {"code": 200, "page_data": page_data, "data": DownloadListAdminSchema().dump(download.items)}


class AddDownloadView(MethodView):
    """添加下载"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddDownloadParse().load(request.values)

        db.session.add(Download(**req_val))
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class DownloadInfoView(MethodView):
    """获取、修改、删除下载"""
    decorators = [admin_login_required]

    def get(self, download_id):
        download = Download.query.filter_by(id=download_id, is_delete=0).first()
        if not download:
            abort(404, description="这个下载不存在")
        return {"code": 200, "data": DownloadInfoSchema().dump(download)}

    def put(self, download_id):
        req_val = UpdateDownloadParse().load(request.values)
        download = Download.query.filter_by(id=download_id, is_delete=0).first()
        if not download:
            abort(404, description="这个下载不存在")
        download.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, download_id):
        download = Download.query.filter_by(id=download_id, is_delete=0).first()
        if not download:
            abort(404, description="这个下载不存在")
        download.delete()
        return {"code": 200, "msg": "删除成功"}
