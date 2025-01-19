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
class StudentSettingsSchema(BaseSchema):
    show_mobile_phone: bool = dataclasses.field(metadata=dict(
        data_key="showMobilePhone", allow_none=True, required=False
    ))
    default_desktop: int = dataclasses.field(metadata=dict(
        data_key="defaultDesktop", allow_none=True, required=False
    ))
    language: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    favorite_reports: list = dataclasses.field(metadata=dict(
        data_key="favoriteReports", allow_none=True, required=False
    ))
    password_expired: int = dataclasses.field(metadata=dict(
        data_key="passwordExpired", allow_none=True, required=False
    ))
    recovery_answer: str = dataclasses.field(metadata=dict(
        data_key="recoveryAnswer", allow_none=True, required=False
    ))
    recovery_question: str = dataclasses.field(metadata=dict(
        data_key="recoveryQuestion", allow_none=True, required=False
    ))
    theme: int = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    user_id: int = dataclasses.field(metadata=dict(
        data_key="userId", allow_none=True, required=False
    ))
    show_netschool_app: bool = dataclasses.field(metadata=dict(
        data_key="showNetSchoolApp", allow_none=True, required=False
    ))
    show_sferum_banner: bool = dataclasses.field(metadata=dict(
        data_key="showSferumBanner", allow_none=True, required=False
    ))


@dataclasses.dataclass
class StudentSchema(BaseSchema):
    user_id: int = dataclasses.field(metadata=dict(
        data_key="userId", allow_none=True, required=False
    ))
    first_name: str = dataclasses.field(metadata=dict(
        data_key="firstName", allow_none=True, required=False
    ))
    last_name: str = dataclasses.field(metadata=dict(
        data_key="lastName", allow_none=True, required=False
    ))
    middle_name: str = dataclasses.field(metadata=dict(
        data_key="middleName", allow_none=True, required=False
    ))
    login: str = dataclasses.field(metadata=dict(
        data_key="loginName", allow_none=True, required=False
    ))
    birthdate: datetime.date = dataclasses.field(metadata=dict(
        data_key="birthDate", allow_none=True, required=False
    ))
    roles: list = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    school_year_id: int = dataclasses.field(metadata=dict(
        data_key="schoolyearId", allow_none=True, required=False
    ))
    mobile_phone: str = dataclasses.field(metadata=dict(
        data_key="mobilePhone", allow_none=True, required=False
    ))
    email: str = dataclasses.field(metadata=dict(
        allow_none=True, required=False
    ))
    exists_photo: bool = dataclasses.field(metadata=dict(
        data_key="existsPhoto", allow_none=True, required=False
    ))
    user_settings: StudentSettingsSchema = dataclasses.field(metadata=dict(
        data_key="userSettings", allow_none=True, required=False
    ))


Student = marshmallow_dataclass.class_schema(StudentSchema)
StudentSettings = marshmallow_dataclass.class_schema(StudentSettingsSchema)