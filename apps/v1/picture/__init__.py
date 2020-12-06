from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/album/list', view_func=PictureAlbumListView.as_view('album_list'))
    api_bp.add_url_rule('/album/<int:album_id>', view_func=PictureAlbumPhotoView.as_view('album_picture'))
    api_bp.add_url_rule('/admin/album/list', view_func=PictureAlbumListAdminView.as_view('admin_album_list'))
    api_bp.add_url_rule('/admin/album', view_func=AddAlbumView.as_view('add_album'))
    api_bp.add_url_rule('/admin/album/<int:album_id>', view_func=PictureAlbumView.as_view('admin_album_picture'))
    api_bp.add_url_rule('/admin/album/picture', view_func=AddPictureView.as_view('add_picture'))
    api_bp.add_url_rule('/admin/album/picture/<int:picture_id>', view_func=PictureInfoView.as_view('admin_picture'))
