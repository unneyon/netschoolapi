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
from .attachment import AttachmentSchema
from .author import AuthorSchema


@dataclasses.dataclass
class AnnouncementSchema(BaseSchema):
    id: int = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    name: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    author: AuthorSchema = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    content: str = dataclasses.field(metadata=dict(
        data_key='description', allow_none=True, required=False
    ))
    post_date: datetime.datetime = dataclasses.field(metadata=dict(
        data_key='postDate', allow_none=True, required=False
    ))
    attachments: typing.List[AttachmentSchema] = dataclasses.field(default_factory=list, metadata=dict(
        allow_none=True, required=False
    ))


Announcement = marshmallow_dataclass.class_schema(AnnouncementSchema)