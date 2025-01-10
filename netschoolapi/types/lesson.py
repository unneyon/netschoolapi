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
from .assignment import AssignmentSchema


@dataclasses.dataclass
class LessonSchema(BaseSchema):
    day: datetime.date
    start: datetime.time = dataclasses.field(metadata={"data_key": "startTime"})
    end: datetime.time = dataclasses.field(metadata={"data_key": "endTime"})
    room: typing.Optional[str] = dataclasses.field(
        metadata={"missing": "", "allow_none": True, "required": False}
    )
    number: int
    subject: str = dataclasses.field(metadata={"data_key": "subjectName"})
    is_distance_lesson: bool = dataclasses.field(metadata={"data_key": "isDistanceLesson"})
    is_ea_lesson: bool = dataclasses.field(metadata={"data_key": "isEaLesson"})
    class_meeting_id: int = dataclasses.field(metadata={"data_key": "classmeetingId"})
    relay: int = dataclasses.field(metadata={"data_key": "relay"})
    assignments: typing.List[AssignmentSchema] = dataclasses.field(default_factory=list)  # type: ignore


Lesson = marshmallow_dataclass.class_schema(LessonSchema)