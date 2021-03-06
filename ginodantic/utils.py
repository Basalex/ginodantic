import keyword
import types
from datetime import datetime
from typing import Any, Type

from gino import json_support
from gino.crud import CRUDModel
from pydantic.dataclasses import dataclass

JSON_FIELDS_MAP = {
    json_support.ArrayProperty: list,
    json_support.StringProperty: str,
    json_support.IntegerProperty: int,
    json_support.BooleanProperty: bool,
    json_support.DateTimeProperty: datetime,
    json_support.ObjectProperty: dict,
}


def get_model_fields(model: Type[CRUDModel]):
    fields = {}
    for field_name in model._column_name_map.keys():
        field = getattr(model, field_name)
        try:
            field_type = field.type.python_type
        except NotImplementedError:
            field_type = str
        fields[field_name] = field, field_type
    for key, prop in model.__dict__.items():
        if isinstance(prop, json_support.JSONProperty):
            fields[key] = getattr(model, key), JSON_FIELDS_MAP.get(type(prop), dict)
            fields.pop(prop.prop_name, None)
    return fields


def make_pydantic_dataclass(
    cls_name,
    fields,
    *,
    bases=(),
    namespace=None,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    config: Type[Any] = None,
    frozen=False,
):
    if namespace is None:
        namespace = {}
    else:
        namespace = namespace.copy()
    seen = set()
    anns = {}
    for item in fields:
        if isinstance(item, str):
            name = item
            tp = "typing.Any"
        elif len(item) == 2:
            name, tp, = item
        elif len(item) == 3:
            name, tp, spec = item
            namespace[name] = spec
        else:
            raise TypeError(f"Invalid field: {item!r}")

        if not isinstance(name, str) or not name.isidentifier():
            raise TypeError(f"Field names must be valid identifiers: {name!r}")
        if keyword.iskeyword(name):
            raise TypeError(f"Field names must not be keywords: {name!r}")
        if name in seen:
            raise TypeError(f"Field name duplicated: {name!r}")

        seen.add(name)
        anns[name] = tp

    namespace["__annotations__"] = anns
    cls = types.new_class(cls_name, bases, {}, lambda ns: ns.update(namespace))
    return dataclass(
        cls,
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
        config=config,
    )
