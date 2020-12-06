from common.marshmallow.base import BaseMarshmallow, PaginateSchema
from flask_marshmallow.fields import fields
from common.marshmallow import validate


# AdminLoginView
class AdminLoginParse(BaseMarshmallow):
    username = fields.String(validate=[validate.str_range(6, 16)], required=True)
    password = fields.String(validate=[validate.str_range(8, 16)], required=True)


# TokenAdminInfoView
class TokenAdminInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "username", "nickname", "avatar", "description")


# GetAdminListView
class GetAdminListParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)
    word = fields.String()


class AdminListSchema(TokenAdminInfoSchema):
    pass


# AdminInfoView
class AdminInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "username", "nickname", "remark", "image_id", "avatar")
    avatar = fields.String(attribute="image.url")


class UpdateAdminInfoParse(BaseMarshmallow):
    password = fields.String(validate=[validate.str_range(8, 16)])
    password_ = fields.String(validate=[validate.str_range(8, 16)])
    nickname = fields.String(validate=[validate.str_range(0, 32)], missing="admin")
    remark = fields.String(validate=[validate.str_range(0, 255)])
    image_id = fields.Integer(validate=[validate.image_exist])


# AddAdminView
class AddAdminParse(BaseMarshmallow):
    username = fields.String(validate=[validate.str_range(6, 16)], required=True)
    password = fields.String(validate=[validate.str_range(8, 16)], required=True)
    password_ = fields.String(validate=[validate.str_range(8, 16)], required=True)
    nickname = fields.String(validate=[validate.str_range(0, 32)], missing="admin")
    remark = fields.String(validate=[validate.str_range(0, 255)])
    image_id = fields.Integer(validate=[validate.image_exist])


