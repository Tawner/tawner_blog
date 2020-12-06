from flask.views import MethodView
from .marshmallows import *
from flask import request, abort
from common.models import Comment
from common.system.login_require import user_login_required, admin_login_required


# 前台接口
class CommentInfoView(MethodView):
    """获取文章评论"""

    def get(self, article_id):
        req_val = CommentInfoParse().load(request.values)

        comment = Comment.query.filter(
            Comment.article_id == article_id,
            Comment.is_delete == 0,
            Comment.theme_id.is_(None)
        ).paginate(req_val['page'], req_val['rows'])
        page_data = PaginateSchema().dump(comment)
        return {"code": 200, "data": CommentListSchema().dump(comment.items)}


class ThemeCommentListView(MethodView):
    """获取主题评论列表"""

    def get(self, theme_id):
        req_val = ThemeCommentListParse().load(request.values)
        comment = Comment.query.filter(
            Comment.theme_id.is_(None),
            Comment.id == theme_id,
            Comment.is_delete == 0
        ).first()
        data = comment.get_page(**req_val)
        comments = data.pop("items")
        return {"code": 200, "page_data": data, "data": SonCommentSchema().dump(comments)}


class AddCommentView(MethodView):
    """添加评论"""
    decorators = [user_login_required]

    def post(self):
        req_val = AddCommentParse().load(request.values)

        result = Comment.add(**req_val)
        if result['status'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "msg": "评论成功"}


# 后台接口
class CommentListView(MethodView):
    """评论列表"""
    decorators = [admin_login_required]

    def get(self):
        req_val = CommentListParse().load(request.values)

        query_args = [Comment.is_delete == 0]
        if "word" in req_val.keys():
            query_args.append(Comment.content.like("%" + req_val['word'] + "%"))
        if "user_id" in req_val.keys():
            query_args.append(Comment.user_id == req_val['user_id'])
        if "article_id" in req_val.keys():
            query_args.append(Comment.article_id == req_val['article_id'])
        comments = Comment.query.filter(*query_args).paginate(req_val['page'], req_val['rows'])

        page_data = PaginateSchema().dump(comments)
        return {"code": 200, "page_data": page_data, "data": CommentListAdminSchema().dump(comments.items)}


class DeleteCommentView(MethodView):
    """删除评论"""
    decorators = [admin_login_required]

    def delete(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id, is_delete=0).first()

        if not comment:
            abort(400, description="该评论不存在")
        comment.delete()
        return {"code": 200, "msg": "删除成功"}

