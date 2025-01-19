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
from .lesson import LessonSchema


@dataclasses.dataclass
class DaySchema(BaseSchema):
    lessons: typing.List[LessonSchema] = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    )) # type: ignore
    day: datetime.date = dataclasses.field(metadata=dict(
        data_key="date", allow_none=True, required=False
    ))


Day = marshmallow_dataclass.class_schema(DaySchema)