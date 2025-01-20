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
    start: datetime.time = dataclasses.field(metadata=dict(
        data_key="startTime", allow_none=True, required=False
    ))
    end: datetime.time = dataclasses.field(metadata=dict(
        data_key="endTime", allow_none=True, required=False
    ))
    room: typing.Optional[str] = dataclasses.field(metadata=dict(
        missing="", allow_none=True, required=False
    ))
    number: int = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    subject: str = dataclasses.field(metadata=dict(
        data_key="subjectName", allow_none=True, required=False
    ))
    is_distance_lesson: bool = dataclasses.field(metadata=dict(
        data_key="isDistanceLesson", allow_none=True, required=False
    ))
    is_ea_lesson: bool = dataclasses.field(metadata=dict(
        data_key="isEaLesson", allow_none=True, required=False
    ))
    class_meeting_id: int = dataclasses.field(metadata=dict(
        data_key="classmeetingId", allow_none=True, required=False
    ))
    relay: int = dataclasses.field(metadata=dict(
        data_key="relay", allow_none=True, required=False
    ))
    assignments: typing.List[AssignmentSchema] = dataclasses.field(default_factory=list, metadata=dict(
        allow_none=True, required=False
    ))  # type: ignore


Lesson = marshmallow_dataclass.class_schema(LessonSchema)