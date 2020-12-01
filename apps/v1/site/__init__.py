from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/site/info', view_func=GetSiteInfoView.as_view('site_info'))
    api_bp.add_url_rule('/social/contact', view_func=GetSocialContactView.as_view('social_contact'))
    api_bp.add_url_rule('/navigation', view_func=GetNavigationView.as_view('navigation'))
    api_bp.add_url_rule('/focusing', view_func=GetFocusingListView.as_view('focusing'))
    api_bp.add_url_rule('/admin/site/info', view_func=SiteInfoView.as_view('admin_site_info'))
    api_bp.add_url_rule('/admin/social/contact', view_func=AddSocialContactView.as_view('add_social_contact'))
    api_bp.add_url_rule('/admin/social/contact/<int:contact_id>', view_func=SocialContactView.as_view('admin_social_contact'))
    api_bp.add_url_rule('/admin/social/contact/list', view_func=SocialContactAdminListView.as_view('admin_social_contact_list'))
    api_bp.add_url_rule('/admin/navigation', view_func=AddNavigationView.as_view('add_navigation'))
    api_bp.add_url_rule('/admin/navigation/<int:navigation_id>', view_func=NavigationInfoView.as_view('admin_navigation_info'))
    api_bp.add_url_rule('/admin/navigation/list', view_func=NavigationAdminListView.as_view('admin_navigation_list'))
    api_bp.add_url_rule('/admin/navigation/url/<int:navigation_url_id>', view_func=NavigationUrlView.as_view('admin_navigation_url'))
    api_bp.add_url_rule('/admin/navigation/url', view_func=AddNavigationUrlView.as_view('add_navigation_url'))
    api_bp.add_url_rule('/admin/focusing', view_func=AddFocusingView.as_view('add_focusing'))
    api_bp.add_url_rule('/admin/focusing/list', view_func=FocusingListAdminView.as_view('admin_focusing_list'))
    api_bp.add_url_rule('/admin/focusing/<int:focus_id>', view_func=FocusingInfoView.as_view('admin_focusing'))




