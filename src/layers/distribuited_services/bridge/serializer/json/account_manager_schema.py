'''This file has the purpose of serving to serialize a account_manager to json format'''
from __future__ import annotations

from marshmallow import fields
from marshmallow import Schema


class AccountManagerSchema(Schema):
    '''Implicit init'''

    uuid = fields.Str()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Int()
    phone_country_code = fields.Int()
    _email = fields.Email()
    created = fields.DateTime()
    modified = fields.DateTime()
    is_active = fields.Boolean()
