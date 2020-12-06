from common.marshmallow.base import BaseMarshmallow, PaginateSchema
from flask_marshmallow.fields import fields
from common.marshmallow import validate
from common.models import Article, Comment, User


class CommentUserSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "nickname", "avatar")


class SonCommentSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "content", "user", "reply_user", "theme_id")
    user = fields.Nested(CommentUserSchema)
    reply_user = fields.Nested(CommentUserSchema, attribute="reply_comment.user")


# CommentInfoView
class CommentInfoParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)


class CommentListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "content", "user", "reply_user", "sub_comment", "theme_id", "more")
    user = fields.Nested(CommentUserSchema)
    reply_user = fields.Nested(CommentUserSchema, attribute="reply_comment.user")
    sub_comment = fields.Nested(SonCommentSchema, many=True)
    more = fields.Boolean(attribute="more_sub_comment")


# ThemeCommentListView
class ThemeCommentListParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)


# AddCommentView
class AddCommentParse(BaseMarshmallow):
    content = fields.String(required=True)
    article_id = fields.Integer(validate=[validate.data_exist(Article)])
    reply_comment_id = fields.Integer(validate=[validate.data_exist(Comment)])


# CommentListView
class CommentListParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)
    word = fields.String()
    article_id = fields.Integer(validate=[validate.data_exist(Article)])
    user_id = fields.Integer(validate=[validate.data_exist(User)])


class CommentListAdminSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "content", "user", "reply_user")
    user = fields.Nested(CommentUserSchema)
    reply_user = fields.Nested(CommentUserSchema, attribute="reply_comment.user")