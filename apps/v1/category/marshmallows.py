from flask_marshmallow.fields import fields
from common.marshmallow.base import BaseMarshmallow
from common.marshmallow import validate
from common.models import *


# CategoryListView
class SubCategorySchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "module")


class CategoryListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "module", "sub")
    sub = fields.Nested(SubCategorySchema, many=True)


# AddCategoryView
class AddCategoryParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(1, 128)], required=True)
    sort = fields.Integer(missing=20)
    module = fields.String(validate=[validate.choice(array=Category.MODULE_TYPE.keys())])
    upper_id = fields.Integer(validate=[validate.category_exist(level=1)])


# CategoryView
class CategoryInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "sort", "module", "upper_id")


class UpdateCategoryParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(1, 128)], required=True)
    sort = fields.Integer(missing=20)
    upper_id = fields.Integer(validate=[validate.category_exist(level=1)])


# CategoryListAdminView
class CategoryListAdminSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "sort", "module", "create_time", "sub")
    sub = fields.Nested(SubCategorySchema, many=True)
    create_time = fields.DateTime('%Y-%m-%d %H:%M')


class CategoryListAdminParse(BaseMarshmallow):
    module = fields.String(validate=[validate.choice(Category.MODULE_TYPE)])


