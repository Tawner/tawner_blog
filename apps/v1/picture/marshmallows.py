from common.marshmallow.base import BaseMarshmallow, PaginateSchema
from flask_marshmallow.fields import fields
from common.marshmallow import validate
from common.models.modules import Picture, PictureAlbum


class CategoryInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "module")


# PictureAlbumListView
class PictureAlbumListParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)
    word = fields.String()
    category = fields.Integer(validate=[validate.category_exist(module="picture")])


class PictureAlbumListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "description", "category", "image", "category_structure")
    image = fields.String(attribute="cover.url")
    category = fields.Nested(CategoryInfoSchema)
    category_structure = fields.Nested(CategoryInfoSchema, attribute="category.structure", many=True)


# PictureAlbumPhotoView
class PictureSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "description", "image", "update_time")
    image = fields.String(attribute="image.url")
    update_time = fields.DateTime("%Y-%m-%d %H:%M")


class PictureAlbumPhotoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "description", "category", "image", "category_structure", "pictures")
    image = fields.String(attribute="cover.url")
    category = fields.Nested(CategoryInfoSchema)
    category_structure = fields.Nested(CategoryInfoSchema, attribute="category.structure", many=True)
    pictures = fields.Nested(PictureSchema, many=True)


# PictureAlbumListAdminView
class PictureAlbumListAdminParse(PictureAlbumListParse):
    pass


class PictureAlbumListAdminSchema(PictureAlbumListSchema):
    pass


# AddAlbumView
class AddAlbumParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(0, 128)], required=True)
    description = fields.String()
    category_id = fields.Integer(validate=[validate.category_exist("picture")], required=True)
    cover_id = fields.Integer(validate=[validate.image_exist], required=True)


# PictureAlbumView
class PictureAdminSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "description", "image", "update_time", "image_id")
    image = fields.String(attribute="image.url")
    update_time = fields.DateTime("%Y-%m-%d %H:%M")


class PictureAlbumSchema(PictureAlbumPhotoSchema):
    picture = fields.Nested(PictureAdminSchema, many=True)


class UpdatePictureAlbumParse(AddAlbumParse):
    pass


# AddPictureView
class AddPictureParse(BaseMarshmallow):
    description = fields.String()
    image_id = fields.Integer(validate=[validate.image_exist], required=True)
    picture_album_id = fields.Integer(validate=[validate.data_exist(PictureAlbum)], required=True)


# PictureInfoView
class PictureInfoParse(BaseMarshmallow):
    description = fields.String()
    image_id = fields.Integer(validate=[validate.image_exist], required=True)







