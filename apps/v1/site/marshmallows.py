from common.marshmallow.base import BaseMarshmallow, PaginateSchema
from flask_marshmallow.fields import fields
from common.marshmallow import validate
from common.models import Navigation, Category


# GetSiteInfoView
class GetSiteInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("name", "slogan", "notice", "case_number", "domain", "host", "avatar", "logo", "background")
    avatar = fields.String(attribute="avatar.url")
    logo = fields.String(attribute="logo.url")
    background = fields.String(attribute="background.url")


# GetSocialContactView
class SocialContactListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "icon", "color", "url")


# GetNavigationView
class FrontNavigationUrlSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "url")


class FrontNavigationListSchema(BaseMarshmallow):
    class Meta:
        fields = ("title", "links")
    links = fields.Nested(FrontNavigationUrlSchema, many=True)


# FocusingListAdminView
class FocusingListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "focus_id", "module", "title", "cover")
    title = fields.String(attribute="focus.title")


# SiteInfoView
class SiteInfoParse(BaseMarshmallow):
    name = fields.String(validate=[validate.str_range(1, 128)], required=True)
    slogan = fields.String(validate=[validate.str_range(1, 255)], required=True)
    notice = fields.String(validate=[validate.str_range(1, 255)], required=True)
    case_number = fields.String(validate=[validate.str_range(1, 255)], required=True)
    domain = fields.String(validate=[validate.str_range(1, 255)], required=True)
    host = fields.String(validate=[validate.str_range(1, 255)], required=True)
    avatar_id = fields.Integer(validate=[validate.image_exist], required=True)
    logo_id = fields.Integer(validate=[validate.image_exist], required=True)
    background_id = fields.Integer(validate=[validate.image_exist], required=True)


class SiteInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("name", "slogan", "notice", "case_number", "domain", "host", "avatar_id", "avatar", "logo_id", "logo", "background_id", "background")
    avatar = fields.String(attribute="avatar.url")
    logo = fields.String(attribute="logo.url")
    background = fields.String(attribute="background.url")


# AddSocialContactView
class AddSocialContactParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(0, 128)], required=True)
    icon = fields.String(validate=[validate.str_range(0, 128)], required=True)
    color = fields.String(validate=[validate.str_range(0, 128)], required=True)
    url = fields.String(validate=[validate.str_range(0, 255)], required=True)
    sort = fields.Integer(validate=[validate.positive], missing=20)


# SocialContactView
class GetSocialContactSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "icon", "color", "url", "sort")


class UpdateSocialContactParse(AddSocialContactParse):
    pass


# SocialContactAdminListView
class SocialContactAdminListSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "icon", "color", "url", "sort")


# AddNavigationView
class AddNavigationParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(1, 128)], required=True)
    sort = fields.Integer(validate=[validate.positive], missing=20)


# NavigationInfoView
class NavigationInfoSchema(BaseMarshmallow):
    class Meta:
        fields = ("title", "sort")


class UpdateNavigationInfoParse(AddNavigationParse):
    pass


# NavigationAdminListView
class NavigationUrlSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "title", "url", "sort")


class NavigationAdminListSchema(BaseMarshmallow):
    class Meta:
        fields = ("title", "sort", "links")
    links = fields.Nested(NavigationUrlSchema, many=True)


# NavigationUrlView
class UpdateNavigationUrlParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(1, 128)], required=True)
    url = fields.String(validate=[validate.str_range(0, 255)])
    sort = fields.Integer(validate=[validate.positive], missing=20)


# AddNavigationUrlView
class AddNavigationUrlParse(BaseMarshmallow):
    title = fields.String(validate=[validate.str_range(1, 128)], required=True)
    url = fields.String(validate=[validate.str_range(0, 255)])
    sort = fields.Integer(validate=[validate.positive], missing=20)
    navigation_id = fields.Integer(validate=[validate.data_exist(Navigation)], required=True)


# AddFocusingView
class AddFocusingParse(BaseMarshmallow):
    module = fields.String(validate=[validate.choice(Category.MODULE_TYPE)], required=True)
    focus_id = fields.Integer(validate=[validate.positive], required=True)
    sort = fields.Integer(validate=[validate.positive], missing=20)


# FocusingListAdminView
class FocusingListAdminSchema(BaseMarshmallow):
    class Meta:
        fields = ("id", "focus_id", "module", "sort", "title", "cover")
    title = fields.String(attribute="focus.title")


# FocusingInfoView
class UpdateFocusingInfoParse(AddFocusingParse):
    pass

