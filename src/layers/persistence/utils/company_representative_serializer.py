'''This file intention is to provide serializer for company representative'''
from __future__ import annotations

from src.layers.domain.model.company_representative import CompanyRepresentative


class CompanyRepresentativeSerializer:
    '''This serializer has the purpose of setting mongo dictionaries
    to domain objects, in this case to a company representative'''

    def __init__(self, mongo_company_representative: dict):

        self.company_representative = CompanyRepresentative(
            'first_name_template', 'last_name_template', '+1000000000',
            'email_template@organization.com', 'email_name_template', '',
        )

        self.company_representative.uuid = mongo_company_representative['uuid']
        self.company_representative.first_name = mongo_company_representative['first_name']
        self.company_representative.last_name = mongo_company_representative['last_name']
        self.company_representative.phone = mongo_company_representative['phone']
        self.company_representative.phone_country_code = mongo_company_representative['phone_country_code']
        self.company_representative._email = mongo_company_representative['_email']
        self.company_representative.password = mongo_company_representative['password']
        self.company_representative.created = mongo_company_representative['created']
        self.company_representative.modified = mongo_company_representative['modified']
        self.company_representative.is_active = mongo_company_representative['is_active']
        self.company_representative.company_uuid = mongo_company_representative['company_uuid']
