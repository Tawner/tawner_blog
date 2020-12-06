from flask.views import MethodView
from .marshmallows import *
from flask import request, abort
from common.models import Download, db
from common.system.login_require import admin_login_required


# 前台接口
class PictureAlbumListView(MethodView):
    """获取图集列表"""

    def get(self):
        req_val = PictureAlbumListParse().load(request.values)
        picture_album = PictureAlbum.list(**req_val)
        page_data = PaginateSchema().dump(picture_album)
        return {"code": 200, "page_data": page_data, "data": PictureAlbumListSchema().dump(picture_album.items)}


class PictureAlbumPhotoView(MethodView):
    """获取图片"""

    def get(self, album_id):
        album = PictureAlbum.query.filter_by(id=album_id, is_delete=0).first()
        if not album:
            abort(400, description="这个图集不存在")
        return {"code": 200, "data": PictureAlbumPhotoSchema().dump(album)}


# 后台接口
class PictureAlbumListAdminView(MethodView):
    """获取图集列表"""
    decorators = [admin_login_required]

    def get(self):
        req_val = PictureAlbumListAdminParse().load(request.values)
        picture_album = PictureAlbum.list(**req_val)
        page_data = PaginateSchema().dump(picture_album)
        return {"code": 200, "page_data": page_data, "data": PictureAlbumListAdminSchema().dump(picture_album.items)}


class AddAlbumView(MethodView):
    """添加图集"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddAlbumParse().load(request.values)
        db.session.add(PictureAlbum(**req_val))
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class PictureAlbumView(MethodView):
    """获取图集修改、删除图集"""
    decorators = [admin_login_required]

    def get(self, album_id):
        album = PictureAlbum.query.filter_by(id=album_id, is_delete=0).first()
        if not album:
            abort(404, description="这个图集不存在")
        return {"code": 200, "data": PictureAlbumSchema().dump(album)}

    def put(self, album_id):
        req_val = UpdatePictureAlbumParse().load(request.values)
        album = PictureAlbum.query.filter_by(id=album_id, is_delete=0).first()
        if not album:
            abort(404, description="这个图集不存在")
        album.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, album_id):
        album = PictureAlbum.query.filter_by(id=album_id, is_delete=0).first()
        if not album:
            abort(404, description="这个图集不存在")
        album.delete()
        return {"code": 200, "msg": "删除成功"}


class AddPictureView(MethodView):
    """添加图片"""
    decorators = [admin_login_required]

    def post(self):
        req_val = AddPictureParse().load(request.values)
        db.session.add(Picture(**req_val))
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class PictureInfoView(MethodView):
    """修改、删除图片"""
    decorators = [admin_login_required]

    def put(self, picture_id):
        req_val = PictureInfoParse().load(request.values)
        picture = Picture.query.filter_by(id=picture_id, is_delete=0).first()
        if not picture:
            abort(404, descriprion="这张图不存在")
        picture.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, picture_id):
        picture = Picture.query.filter_by(id=picture_id, is_delete=0).first()
        if not picture:
            abort(404, descriprion="这张图不存在")
        picture.delete()
        return {"code": 200, "msg": "删除成功"}

