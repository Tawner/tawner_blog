from common.marshmallow.base import BaseMarshmallow, PaginateSchema
from flask_marshmallow.fields import fields
from common.marshmallow import validate


# UserLoginView
class UserLoginParse(BaseMarshmallow):
    username = fields.Email(validate=[validate.str_range(0, 128)], required=True)
    password = fields.String(validate=[validate.str_range(8, 16)], required=True)


# UserRegisterView
class UserRegisterParse(BaseMarshmallow):
    email = fields.Email(validate=[validate.str_range(0, 128)], required=True)
    password = fields.String(validate=[validate.str_range(8, 16)], required=True)
    password_ = fields.String(validate=[validate.str_range(8, 16)], required=True)
    code = fields.String(validate=[validate.str_range(6, 6)], required=True)


# SendEmailCodeView
class SendEmailCodeParse(BaseMarshmallow):
    email = fields.Email(validate=[validate.str_range(0, 128)], required=True)


# TokenUserInfoView
class TokenUserInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("email", "nickname", "description", "gender", "image_id", "avatar")
    avatar = fields.String(attribute="image.url")


class UpdateUserInfoParse(BaseMarshmallow):
    nickname = fields.String(validate=[validate.str_range(0, 32)])
    description = fields.String(validate=[validate.str_range(0, 255)])
    gender = fields.Integer(validate=[validate.choice([0, 1, 2])], missing=0)
    image_id = fields.Integer(validate=[validate.image_exist])


# UserModifyPasswordView
class UserModifyPasswordParse(BaseMarshmallow):
    password = fields.String(validate=[validate.str_range(8, 16)], required=True)
    password_ = fields.String(validate=[validate.str_range(8, 16)], required=True)
    code = fields.String(validate=[validate.str_range(6, 6)], required=True)


# UserListView
class UserListParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)
    word = fields.String()


class UserListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "email", "nickname", "description", "gender", "image_id", "avatar")
    avatar = fields.String(attribute="image.url")

