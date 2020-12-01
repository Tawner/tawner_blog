from . import marshmallow
from collections import Iterable
from flask_marshmallow.fields import fields


class BaseMarshmallow(marshmallow.Schema):
    def __init__(self, *args, **kwargs):
        if 'unknown' not in kwargs.keys():
            kwargs['unknown'] = "exclude"
        super().__init__(*args, **kwargs)

    def dump(self, *args, **kwargs):
        obj = args[0] if len(args) > 0 else kwargs.get('obj', None)
        if isinstance(obj, Iterable):
            self.many = True
        return super().dump(*args, **kwargs)


# 通用
class PaginateSchema(BaseMarshmallow):
    class Meta:
        fields = ("page", "pages", "rows", "has_next", "has_prev", "total")

    rows = fields.Integer(attribute="per_page")
