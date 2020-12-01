from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/article/list', view_func=ArticleListView.as_view('article_list'))
    api_bp.add_url_rule('/article/<int:article_id>', view_func=ArticleInfoView.as_view('article_info'))
    api_bp.add_url_rule('/admin/article', view_func=AddArticleView.as_view('add_article'))
    api_bp.add_url_rule('/admin/article/<int:article_id>', view_func=ArticleInfoAdminView.as_view('admin_article_info'))
    api_bp.add_url_rule('/admin/article/list', view_func=ArticleListAdminView.as_view('admin_article_list'))






