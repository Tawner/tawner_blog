from common.marshmallow.base import *
from common.marshmallow import validate
from common.models import *


class CategoryInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "module")


class ArticleListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "comment", "view", "image", "category", "top", "publish_date", "description", "recom", "hot")
    publish_date = fields.DateTime("%Y-%m-%d")
    image = fields.String(attribute="cover.url")
    category = fields.Nested(CategoryInfoSchema)


class TagInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "name")


# ArticleListView
class ArticleListParse(BaseMarshmallow):
    page = fields.Integer(validate=[validate.positive], missing=1)
    rows = fields.Integer(validate=[validate.positive], missing=10)
    word = fields.String()
    recom = fields.Boolean(missing=False)
    category = fields.Integer(validate=[validate.category_exist(module="article")])


# ArticleInfoView
class ArticleInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "content", "comment", "view", "published_date", "description", "category_id", "image", "category_structure", "tags")
    publish_date = fields.DateTime("%Y-%m-%d %H:%M")
    image = fields.String(attribute="cover.url")
    category_structure = fields.Nested(CategoryInfoSchema, attribute="category.structure")
    tags = fields.Nested(TagInfoSchema)


# AddArticleView
class AddArticleParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(1, 255)], required=True)
    content = fields.String()
    recom = fields.Boolean(missing=False)
    top = fields.Boolean(missing=False)
    published = fields.Boolean(missing=True)
    publish_date = fields.DateTime('%Y-%m-%d %H:%M')
    description = fields.String()
    cover_id = fields.Integer(validate=[validate.image_exist], required=True)
    category_id = fields.Integer(validate=[validate.category_exist("article")], required=True)
    tag_id = fields.List(fields.Integer(validate=[validate.data_exist(Tag)]))


# ArticleInfoAdminView
class ArticleInfoAdminSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "content", "comment", "view", "recom", "top", "published", "published_date", "description", "cover_id", "category_id", "image", "category_structure", "tags")
    publish_date = fields.DateTime("%Y-%m-%d %H:%M")
    image = fields.String(attribute="cover.url")
    category_structure = fields.Nested(CategoryInfoSchema, attribute="category.structure")
    tags = fields.Nested(TagInfoSchema)


class UpdateArticleInfo(AddArticleParse):
    pass


# ArticleListAdminView
class ArticleListAdminParse(ArticleListParse):
    published = fields.Boolean()


class ArticleListAdminSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "comment", "view", "image", "category", "top", "publish_date", "recom", "published")
    publish_date = fields.DateTime("%Y-%m-%d")
    image = fields.String(attribute="cover.url")
    category = fields.Nested(CategoryInfoSchema)



