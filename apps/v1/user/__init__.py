from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/user/login', view_func=UserLoginView.as_view('user_login'))
    api_bp.add_url_rule('/user/logout', view_func=UserLogoutView.as_view('user_logout'))
    api_bp.add_url_rule('/user/register', view_func=UserRegisterView.as_view('user_register'))
    api_bp.add_url_rule('/email/validate', view_func=SendEmailCodeView.as_view('send_email'))
    api_bp.add_url_rule('/user/info', view_func=TokenUserInfoView.as_view('user_token_info'))
    api_bp.add_url_rule('/user/password', view_func=UserModifyPasswordView.as_view('user_modify_password'))
    api_bp.add_url_rule('/admin/user/list', view_func=UserListView.as_view('user_list'))
    api_bp.add_url_rule('/admin/user/<int:user_id>', view_func=DeleteUserView.as_view('delete_user'))






