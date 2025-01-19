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

import marshmallow


@dataclasses.dataclass
class BaseSchema(marshmallow.Schema):
    class Meta:
        dateformat = '%Y-%m-%dT00:00:00'
        unknown = marshmallow.EXCLUDE


class UnionField(marshmallow.fields.Field):
    def __init__(self, *types, **kwargs):
        self.types = types
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        for t in self.types:
            try:
                return t(value)
            except (ValueError, TypeError):
                continue
        self.fail("invalid")