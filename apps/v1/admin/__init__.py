from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/admin/login', view_func=AdminLoginView.as_view('admin_login'))
    api_bp.add_url_rule('/admin/logout', view_func=AdminLogoutView.as_view('admin_logout'))
    api_bp.add_url_rule('/admin/token/info', view_func=TokenAdminInfoView.as_view('token_info'))
    api_bp.add_url_rule('/admin/backend/user/list', view_func=GetAdminListView.as_view('admin_list'))
    api_bp.add_url_rule('/admin/backend/user/info/<int:admin_id>', view_func=AdminInfoView.as_view('admin_info'))
    api_bp.add_url_rule('/admin/backend/user/info', view_func=AddAdminView.as_view('add_admin'))

