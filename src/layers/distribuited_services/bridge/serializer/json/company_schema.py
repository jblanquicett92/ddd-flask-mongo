'''This file has the purpose of serving to serialize a company to json format'''
from __future__ import annotations

from marshmallow import fields
from marshmallow import Schema


class CompanySchema(Schema):
    '''Implicit init'''

    uuid = fields.Str()
    name = fields.Str()
    phone = fields.Str()
    created = fields.Str()
    modified = fields.Str()
    is_active = fields.Boolean()
    email = fields.Str()
