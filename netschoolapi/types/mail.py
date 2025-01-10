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


@dataclasses.dataclass
class MessageMinSchema(BaseSchema):
    id: int = dataclasses.field(metadata=dict(data_key='id'))
    date: datetime.datetime = dataclasses.field(metadata=dict(data_key='sent'))
    message_subject: str = dataclasses.field(metadata=dict(data_key='subject'))
    author: str | None = dataclasses.field(metadata=dict(data_key='author'))
    to_names: str | None = dataclasses.field(metadata=dict(data_key='toNames'))


@dataclasses.dataclass
class MessagesSchema(BaseSchema):
    fields: list = dataclasses.field(metadata=dict(data_key='fields'))
    page: int = dataclasses.field(metadata=dict(data_key='page'))
    total: int = dataclasses.field(metadata=dict(data_key='totalItems'))
    rows: typing.List[MessageMinSchema] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class MessageAuthorSchema(BaseSchema):
    id: int | str
    name: str
    organization_name: str  = dataclasses.field(metadata=dict(
        data_key='organizationName', allow_none=True, missing='', required=False
    ))
    is_group_recipient: bool = dataclasses.field(metadata=dict(
        data_key='isGroupRecipient', allow_none=True, missing='', required=False
    ))
    sub_recipients: str = dataclasses.field(metadata=dict(
        data_key='subRecipients', allow_none=True, missing='', required=False
    ))

@dataclasses.dataclass
class MessageSchema(BaseSchema):
    id: int
    text: str
    message_subject: str = dataclasses.field(metadata=dict(data_key='subject'))
    notify: bool = dataclasses.field(metadata=dict(data_key='notify'))
    date: datetime.datetime = dataclasses.field(metadata=dict(data_key='sent'))
    author: MessageAuthorSchema = dataclasses.field(metadata=dict(data_key='author'))
    attachments: typing.List[AttachmentSchema] = dataclasses.field(metadata=dict(data_key='fileAttachments'))
    to: typing.List[MessageAuthorSchema] = dataclasses.field(metadata=dict(data_key='to'))
    to_names: str = dataclasses.field(metadata=dict(data_key='toNames'))
    mailBox: str = dataclasses.field(metadata=dict(data_key='mailBox'))
    noReply: bool = dataclasses.field(metadata=dict(data_key='noReply'))
    read: bool = dataclasses.field(metadata=dict(data_key='read'))
    canReplyAll: bool = dataclasses.field(metadata=dict(data_key='canReplyAll'))
    canForward: bool = dataclasses.field(metadata=dict(data_key='canForward'))
    canEdit: bool = dataclasses.field(metadata=dict(data_key='canEdit'))


MessageMin = marshmallow_dataclass.class_schema(MessageMinSchema)
Messages = marshmallow_dataclass.class_schema(MessagesSchema)
MessageAuthor = marshmallow_dataclass.class_schema(MessageAuthorSchema)
Message = marshmallow_dataclass.class_schema(MessageSchema)