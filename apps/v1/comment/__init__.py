from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/comment/<int:article_id>', view_func=CommentInfoView.as_view('comment_info'))
    api_bp.add_url_rule('/comment/theme/<int:theme_id>', view_func=ThemeCommentListView.as_view('theme_list'))
    api_bp.add_url_rule('/comment', view_func=AddCommentView.as_view('add_comment'))
    api_bp.add_url_rule('/admin/comment/list', view_func=CommentListView.as_view('comment_list'))
    api_bp.add_url_rule('/admin/comment/<int:comment_id>', view_func=DeleteCommentView.as_view('delete_comment'))
