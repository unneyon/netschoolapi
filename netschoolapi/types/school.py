#          █  █ █▄ █ █▄ █ █▀▀ ▀▄▀ █▀█ █▄ █
#          ▀▄▄▀ █ ▀█ █ ▀█ ██▄  █  █▄█ █ ▀█ ▄
#                © Copyright 2024
#            ✈ https://t.me/unneyon

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit this file without direct permission from the author.
# You can redistribute this file without any changes.

import dataclasses
import datetime
import typing

import marshmallow
import marshmallow_dataclass

from ._base import BaseSchema


@dataclasses.dataclass
class ShortSchoolSchema(BaseSchema):
    name: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    id: int = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    address: str = dataclasses.field(metadata=dict(
        data_key="addressString", allow_none=True, required=False
    ))


@dataclasses.dataclass
class SchoolSchema(BaseSchema):
    name: str = dataclasses.field(metadata=dict(
        data_key="fullSchoolName3", allow_none=True, required=False
    ))
    about: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))

    address: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    email: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    site: str = dataclasses.field(metadata=dict(
        data_key="web", allow_none=True, required=False
    ))
    phone: str = dataclasses.field(metadata=dict(
        data_key="phones", allow_none=True, required=False
    ))

    director: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    AHC: str = dataclasses.field(metadata=dict(
        data_key="principalAHC", allow_none=True, required=False
    ))
    IT: str = dataclasses.field(metadata=dict(
        data_key="principalIT", allow_none=True, required=False
    ))
    UVR: str = dataclasses.field(metadata=dict(
        data_key="principalUVR", allow_none=True, required=False
    ))

    @marshmallow.pre_load
    def unwrap_nested_dicts(
            self, school: typing.Dict[str, typing.Any], **_) -> typing.Dict[str, str]:
        school.update(school.pop("commonInfo"))
        school.update(school.pop("contactInfo"))
        school.update(school.pop("managementInfo"))
        school['address'] = school['juridicalAddress'] or school['postAddress']
        return school


ShortSchool = marshmallow_dataclass.class_schema(ShortSchoolSchema)
School = marshmallow_dataclass.class_schema(SchoolSchema)