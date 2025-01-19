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
class AssignmentSchema(BaseSchema):
    id: int = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    comment: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    type: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    content: str = dataclasses.field(metadata=dict(
        data_key="assignmentName", allow_none=True, required=False
    ))
    mark: typing.Optional[int] = dataclasses.field(metadata=dict(
        data_key="mark", allow_none=True, required=False
    ))
    is_duty: bool = dataclasses.field(metadata=dict(
        data_key="dutyMark", allow_none=True, required=False
    ))
    deadline: datetime.date = dataclasses.field(metadata=dict(
        data_key="dueDate", allow_none=True, required=False
    ))

    @marshmallow.pre_load
    def unwrap_marks(self, assignment: typing.Dict[str, typing.Any], **_) -> typing.Dict[str, typing.Any]:
        mark = assignment.pop("mark", None)
        if mark:
            assignment.update(mark)
        else:
            assignment.update({"mark": None, "dutyMark": False})
        mark_comment = assignment.pop("markComment", None)
        assignment["comment"] = mark_comment["name"] if mark_comment else ""
        assignment["type"] = self.context["assignment_types"][assignment.pop("typeId")]
        return assignment


Assignment = marshmallow_dataclass.class_schema(AssignmentSchema)