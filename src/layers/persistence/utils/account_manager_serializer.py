'''This file intention is to provide serializer for account manager'''
from __future__ import annotations

from src.layers.domain.model.account_manager import AccountManager


class AccountManagerSerializer:
    '''This serializer has the purpose of setting mongo dictionaries
    to domain objects, in this case to a account manager'''

    def __init__(self, mongo_account_manager: dict):

        self.account_manager = AccountManager(
            'first_name_template', 'last_name_template', '+1000000000',
            'email_template@organization.com', 'email_name_template',
        )

        self.account_manager.uuid = mongo_account_manager['uuid']
        self.account_manager.first_name = mongo_account_manager['first_name']
        self.account_manager.last_name = mongo_account_manager['last_name']
        self.account_manager.phone = mongo_account_manager['phone']
        self.account_manager.phone_country_code = mongo_account_manager['phone_country_code']
        self.account_manager._email = mongo_account_manager['_email']
        self.account_manager.password = mongo_account_manager['password']
        self.account_manager.created = mongo_account_manager['created']
        self.account_manager.modified = mongo_account_manager['modified']
        self.account_manager.is_active = mongo_account_manager['is_active']
