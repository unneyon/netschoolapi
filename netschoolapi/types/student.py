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
    show_mobile_phone: bool = dataclasses.field(metadata=dict(data_key='showMobilePhone'))
    default_desktop: int = dataclasses.field(metadata=dict(data_key='defaultDesktop'))
    language: str
    favorite_reports: list = dataclasses.field(metadata=dict(data_key='favoriteReports'))
    password_expired: int = dataclasses.field(metadata=dict(data_key='passwordExpired'))
    recovery_answer: str = dataclasses.field(metadata=dict(data_key='recoveryAnswer'))
    recovery_question: str = dataclasses.field(metadata=dict(data_key='recoveryQuestion'))
    theme: int
    user_id: int = dataclasses.field(metadata=dict(data_key='userId'))
    show_netschool_app: bool = dataclasses.field(metadata=dict(data_key='showNetSchoolApp'))
    show_sferum_banner: bool = dataclasses.field(metadata=dict(data_key='showSferumBanner'))


@dataclasses.dataclass
class StudentSchema(BaseSchema):
    user_id: int = dataclasses.field(metadata=dict(data_key='userId'))
    first_name: str = dataclasses.field(metadata=dict(data_key='firstName'))
    last_name: str = dataclasses.field(metadata=dict(data_key='lastName'))
    middle_name: str = dataclasses.field(metadata=dict(data_key='middleName'))
    login: str = dataclasses.field(metadata=dict(data_key='loginName'))
    birthdate: datetime.date = dataclasses.field(metadata=dict(data_key='birthDate'))
    roles: list
    school_year_id: int = dataclasses.field(metadata=dict(data_key='schoolyearId'))
    mobile_phone: str = dataclasses.field(metadata=dict(data_key='mobilePhone'))
    email: str = dataclasses.field(metadata=dict(data_key='email'))
    exists_photo: bool = dataclasses.field(metadata=dict(data_key='existsPhoto'))
    user_settings: StudentSettingsSchema = dataclasses.field(metadata=dict(data_key='userSettings'))


Student = marshmallow_dataclass.class_schema(StudentSchema)
StudentSettings = marshmallow_dataclass.class_schema(StudentSettingsSchema)