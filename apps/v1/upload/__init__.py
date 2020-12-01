from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/upload', view_func=UploadView.as_view('upload'))
    api_bp.add_url_rule('/upload/editor', view_func=EditorUploadView.as_view('editor_upload'))





