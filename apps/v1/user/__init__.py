from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/email/validate', view_func=EmailValidateView.as_view('email_validate'))
    # api_bp.add_url_rule('/upload/editor', view_func=EditorUploadView.as_view('editor_upload'))





