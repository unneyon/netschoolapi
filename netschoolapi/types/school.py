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
    name: str
    id: int
    address: str = dataclasses.field(metadata=dict(data_key="addressString"))


@dataclasses.dataclass
class SchoolSchema(BaseSchema):
    name: str = dataclasses.field(metadata=dict(data_key='fullSchoolName3'))
    about: str

    address: str
    email: str
    site: str = dataclasses.field(metadata=dict(data_key='web'))
    phone: str = dataclasses.field(metadata=dict(data_key='phones'))

    director: str
    AHC: str = dataclasses.field(metadata=dict(data_key='principalAHC'))
    IT: str = dataclasses.field(metadata=dict(data_key='principalIT'))
    UVR: str = dataclasses.field(metadata=dict(data_key='principalUVR'))

    @marshmallow.pre_load
    def unwrap_nested_dicts(
            self, school: typing.Dict[str, typing.Any], **_) -> typing.Dict[str, str]:
        school.update(school.pop('commonInfo'))
        school.update(school.pop('contactInfo'))
        school.update(school.pop('managementInfo'))
        school['address'] = school['juridicalAddress'] or school['postAddress']
        return school


ShortSchool = marshmallow_dataclass.class_schema(ShortSchoolSchema)
School = marshmallow_dataclass.class_schema(SchoolSchema)