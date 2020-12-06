from common.marshmallow.base import BaseMarshmallow, PaginateSchema
from flask_marshmallow.fields import fields
from common.marshmallow import validate
from common.models.modules import Download
from common.models import Upload


class CategoryInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "module")


# DownloadListView
class DownloadListParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)
    word = fields.String()
    category = fields.Integer(validate=[validate.category_exist(module="download")])


class DownloadListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "description", "version", "frequency", "language", "size", "image", "category_structure", "category_id", "category", "update_time")
    update_time = fields.DateTime("%Y-%m-%d")
    image = fields.String(attribute="cover.url")
    category = fields.Nested(CategoryInfoSchema)
    category_structure = fields.Nested(CategoryInfoSchema, attribute="category.structure")
    size = fields.String(attribute="file.size")


# DownloadListAdminView
class DownloadListAdminParse(DownloadListParse):
    pass


class DownloadListAdminSchema(DownloadListSchema):
    pass


# AddDownloadView
class AddDownloadParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(0, 128)], required=True)
    description = fields.String()
    version = fields.String(validate=[validate.str_range(0, 64)])
    language = fields.String(validate=[validate.str_range(0, 128)])
    file_id = fields.Integer(validate=[validate.data_exist(Upload)], required=True)
    category_id = fields.Integer(validate=[validate.category_exist("download")], required=True)
    cover_id = fields.Integer(validate=[validate.image_exist], required=True)


# DownloadInfoView
class DownloadInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "description", "version", "language", "file_id", "category_id", "cover_id", "image")
    image = fields.String(attribute="cover.url")


class UpdateDownloadParse(AddDownloadParse):
    pass


