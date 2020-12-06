from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/article/list', view_func=ArticleListView.as_view('article_list'))
    api_bp.add_url_rule('/article/<int:article_id>', view_func=ArticleInfoView.as_view('article_info'))
    api_bp.add_url_rule('/article/tag/list', view_func=ArticleTagListView.as_view('article_tag'))
    api_bp.add_url_rule('/article/tag/<int:tag_id>', view_func=TagArticleListView.as_view('tag_article_list'))
    api_bp.add_url_rule('/admin/article', view_func=AddArticleView.as_view('add_article'))
    api_bp.add_url_rule('/admin/article/<int:article_id>', view_func=ArticleInfoAdminView.as_view('admin_article_info'))
    api_bp.add_url_rule('/admin/article/list', view_func=ArticleListAdminView.as_view('admin_article_list'))
    api_bp.add_url_rule('/admin/article/tag', view_func=AddTagView.as_view('add_tag'))
    api_bp.add_url_rule('/admin/article/tag/list', view_func=TagListAdminView.as_view('admin_tag_list'))
    api_bp.add_url_rule('/admin/article/tag/<int:tag_id>', view_func=TagInfoAdminView.as_view('admin_tag_info'))







