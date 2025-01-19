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

from ._base import BaseSchema, UnionField
from .attachment import AttachmentSchema


@dataclasses.dataclass
class MessageMinSchema(BaseSchema):
    id: typing.Any = dataclasses.field(metadata=dict(
        marshmallow_field=UnionField(str, int, allow_none=True, required=False)
    ))
    date: datetime.datetime = dataclasses.field(metadata=dict(
        data_key="sent", allow_none=True, required=False
    ))
    message_subject: str = dataclasses.field(metadata=dict(
        data_key="subject", allow_none=True, required=False
    ))
    author: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    to_names: str = dataclasses.field(metadata=dict(
        data_key="toNames", allow_none=True, required=False
    ))


@dataclasses.dataclass
class MessagesSchema(BaseSchema):
    fields: list = dataclasses.field(metadata=dict(
        data_key="fields", allow_none=True, required=False
    ))
    page: int = dataclasses.field(metadata=dict(
        data_key="page", allow_none=True, required=False
    ))
    total: int = dataclasses.field(metadata=dict(
        data_key="totalItems", allow_none=True, required=False
    ))
    rows: typing.List[MessageMinSchema] = dataclasses.field(default_factory=list, metadata=dict(
        allow_none=True, required=False
    ))


@dataclasses.dataclass
class MessageAuthorSchema(BaseSchema):
    id: typing.Any = dataclasses.field(metadata=dict(
        marshmallow_field=UnionField(str, int, allow_none=True, required=False)
    ))
    name: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    organization_name: str  = dataclasses.field(metadata=dict(
        data_key="organizationName", allow_none=True, missing='', required=False
    ))
    is_group_recipient: bool = dataclasses.field(metadata=dict(
        data_key="isGroupRecipient", allow_none=True, missing='', required=False
    ))
    sub_recipients: str = dataclasses.field(metadata=dict(
        data_key="subRecipients", allow_none=True, missing='', required=False
    ))

@dataclasses.dataclass
class MessageSchema(BaseSchema):
    id: int = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    text: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    message_subject: str = dataclasses.field(metadata=dict(
        data_key="subject", allow_none=True, required=False
    ))
    notify: bool = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    date: datetime.datetime = dataclasses.field(metadata=dict(
        data_key="sent", allow_none=True, required=False
    ))
    author: MessageAuthorSchema = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    attachments: typing.List[AttachmentSchema] = dataclasses.field(metadata=dict(
        data_key="fileAttachments", allow_none=True, required=False
    ))
    to: typing.List[MessageAuthorSchema] = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    to_names: str = dataclasses.field(metadata=dict(
        data_key="toNames", allow_none=True, required=False
    ))
    mail_box: str = dataclasses.field(metadata=dict(
        data_key="mailBox", allow_none=True, required=False
    ))
    no_reply: bool = dataclasses.field(metadata=dict(
        data_key="noReply", allow_none=True, required=False
    ))
    read: bool = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    can_reply_all: bool = dataclasses.field(metadata=dict(
        data_key="canReplyAll", allow_none=True, required=False
    ))
    can_forward: bool = dataclasses.field(metadata=dict(
        data_key="canForward", allow_none=True, required=False
    ))
    can_edit: bool = dataclasses.field(metadata=dict(
        data_key="canEdit", allow_none=True, required=False
    ))


MessageMin = marshmallow_dataclass.class_schema(MessageMinSchema)
Messages = marshmallow_dataclass.class_schema(MessagesSchema)
MessageAuthor = marshmallow_dataclass.class_schema(MessageAuthorSchema)
Message = marshmallow_dataclass.class_schema(MessageSchema)