from common.marshmallow.base import BaseMarshmallow, PaginateSchema
from flask_marshmallow.fields import fields
from common.marshmallow import validate
from common.models import Navigation, Category


# UserLoginView
class UserLoginParse(BaseMarshmallow):
    username = fields.String(validate=[validate.str_range(6, 16)], required=True)
    password = fields.String(validate=[validate.str_range(6, 16)], required=True)


# UserInfoView
class UserInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("username", "nickname", "description", "gender", "email", "avatar", "image_id")
    avatar = fields.String(attribute="image.url")


class UpdateUserInfoParse(BaseMarshmallow):
    password = fields.String(validate=[validate.str_range(6, 16)])
    password_ = fields.String(validate=[validate.str_range(6, 16)])
    nickname = fields.String(validate=[validate.str_range(1, 32)], required=True)
    description = fields.String(validate=[validate.str_range(0, 255)])
    gender = fields.Integer(validate=[validate.choice([0, 1, 2])], missing=0)
    email = fields.Email(validate=[validate.str_range(0, 128)], required=True)
    image_id = fields.Integer(validate=[validate.image_exist])


# EmailValidateView
class EmailValidateParse(BaseMarshmallow):
    email = fields.Email(validate=[validate.str_range(0, 128)], required=True)

