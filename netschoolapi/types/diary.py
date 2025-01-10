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
from .day import DaySchema


@dataclasses.dataclass
class DiarySchema(BaseSchema):
    start: datetime.date = dataclasses.field(metadata={"data_key": "weekStart"})
    end: datetime.date = dataclasses.field(metadata={"data_key": "weekEnd"})
    schedule: typing.List[DaySchema] = dataclasses.field(metadata={"data_key": "weekDays"})  # type: ignore


Diary = marshmallow_dataclass.class_schema(DiarySchema)