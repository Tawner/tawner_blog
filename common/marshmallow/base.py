from . import marshmallow
from collections import Iterable
from flask_marshmallow.fields import fields

# 重写_deserialize导入模块
from collections.abc import Mapping
import typing
from marshmallow.error_store import ErrorStore
from marshmallow.utils import (
    RAISE,
    EXCLUDE,
    INCLUDE,
    missing,
    set_value,
    is_collection,

)
_T = typing.TypeVar("_T")


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

    def _deserialize(
        self,
        data: typing.Union[
            typing.Mapping[str, typing.Any],
            typing.Iterable[typing.Mapping[str, typing.Any]],
        ],
        *,
        error_store: ErrorStore,
        many: bool = False,
        partial=False,
        unknown=RAISE,
        index=None
    ) -> typing.Union[_T, typing.List[_T]]:
        """Deserialize ``data``.

        :param dict data: The data to deserialize.
        :param ErrorStore error_store: Structure to store errors.
        :param bool many: `True` if ``data`` should be deserialized as a collection.
        :param bool|tuple partial: Whether to ignore missing fields and not require
            any fields declared. Propagates down to ``Nested`` fields as well. If
            its value is an iterable, only missing fields listed in that iterable
            will be ignored. Use dot delimiters to specify nested fields.
        :param unknown: Whether to exclude, include, or raise an error for unknown
            fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
        :param int index: Index of the item being serialized (for storing errors) if
            serializing a collection, otherwise `None`.
        :return: A dictionary of the deserialized data.
        """
        index_errors = self.opts.index_errors
        index = index if index_errors else None
        if many:
            if not is_collection(data):
                error_store.store_error([self.error_messages["type"]], index=index)
                ret = []  # type: typing.List[_T]
            else:
                ret = [
                    typing.cast(
                        _T,
                        self._deserialize(
                            typing.cast(typing.Mapping[str, typing.Any], d),
                            error_store=error_store,
                            many=False,
                            partial=partial,
                            unknown=unknown,
                            index=idx,
                        ),
                    )
                    for idx, d in enumerate(data)
                ]
            return ret
        ret = self.dict_class()
        # Check data is a dict
        if not isinstance(data, Mapping):
            error_store.store_error([self.error_messages["type"]], index=index)
        else:
            partial_is_collection = is_collection(partial)
            for attr_name, field_obj in self.load_fields.items():
                field_name = (
                    field_obj.data_key if field_obj.data_key is not None else attr_name
                )

                # 解决fields.List，不能正确获取字段
                from flask_marshmallow.fields import fields
                raw_value = data.getlist(field_name) if isinstance(field_obj, fields.List) else data.get(field_name, missing)

                if raw_value is missing:
                    # Ignore missing field if we're allowed to.
                    if partial is True or (
                        partial_is_collection and attr_name in partial
                    ):
                        continue
                d_kwargs = {}
                # Allow partial loading of nested schemas.
                if partial_is_collection:
                    prefix = field_name + "."
                    len_prefix = len(prefix)
                    sub_partial = [
                        f[len_prefix:] for f in partial if f.startswith(prefix)
                    ]
                    d_kwargs["partial"] = sub_partial
                else:
                    d_kwargs["partial"] = partial
                getter = lambda val: field_obj.deserialize(
                    val, field_name, data, **d_kwargs
                )
                value = self._call_and_store(
                    getter_func=getter,
                    data=raw_value,
                    field_name=field_name,
                    error_store=error_store,
                    index=index,
                )
                if value is not missing:
                    key = field_obj.attribute or attr_name
                    set_value(typing.cast(typing.Dict, ret), key, value)
            if unknown != EXCLUDE:
                fields = {
                    field_obj.data_key if field_obj.data_key is not None else field_name
                    for field_name, field_obj in self.load_fields.items()
                }
                for key in set(data) - fields:
                    value = data[key]
                    if unknown == INCLUDE:
                        set_value(typing.cast(typing.Dict, ret), key, value)
                    elif unknown == RAISE:
                        error_store.store_error(
                            [self.error_messages["unknown"]],
                            key,
                            (index if index_errors else None),
                        )
        return ret


# 通用
class PaginateSchema(BaseMarshmallow):
    class Meta:
        fields = ("page", "pages", "rows", "has_next", "has_prev", "total")

    rows = fields.Integer(attribute="per_page")
