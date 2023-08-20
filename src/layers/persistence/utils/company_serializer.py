'''This file intention is to provide serializer for company'''
from __future__ import annotations

from src.layers.domain.model.company import Company


class CompanySerializer:
    '''This serializer has the purpose of setting mongo dictionaries
    to domain objects, in this case to a company'''

    def __init__(self, mongo_company: dict):

        self.company = Company('', '')
        self.company.uuid = mongo_company['uuid']
        self.company.name = mongo_company['name']
        self.company.phone = mongo_company['phone']
        self.company.created = mongo_company['created']
        self.company.modified = mongo_company['modified']
        self.company.is_active = mongo_company['is_active']
        self.company.email = mongo_company['email']
