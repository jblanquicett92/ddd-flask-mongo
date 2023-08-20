'''This file intention is to provide the class company
and its business rules'''
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

import pandas as pd
from decouple import config as environment

from src.layers.domain.model.company_representative import CompanyRepresentative
from src.layers.domain.model.company_representative_dictionary import (
    CompanyRepresentativeDictionary,
)
from src.layers.domain.model.user import User
from src.layers.domain.model.user_dictionary import UserDictionary


@dataclass
class Company:
    """Company interested in its employees being able to move from
     home to work more efficiently and quickly"""

    def __init__(self, name, phone, email=None) -> None:

        self.uuid = self.__generate_uuid()
        self.name = name
        self.phone = phone
        self.email = email
        self.created = self.__created_at()
        self.modified = self.__modified_at()
        self.is_active = True
        self._users = UserDictionary()
        self._company_representatives = CompanyRepresentativeDictionary()

    def __created_at(self):
        return str(datetime.now())

    def __modified_at(self):
        return str(datetime.now())

    def __generate_uuid(self):
        return str(uuid4())

    def users(self) -> dict:
        """return a dict of all users by company"""
        return self._users

    def users_active(self):
        """return a dict of active users by company"""
        return [
            {user.uuid: user} for user in self._users.values() if user.is_active is True
        ]

    def users_assigned_credit_more_than(self, value: int):
        """return a dict of users by company that assigned credit more than a value"""
        return [
            {user.uuid: user}
            for user in self._users.values()
            if user.asigned_credits > value
        ]

    def users_assigned_credit_less_than(self, value: int):
        """return a dict of users by company that assigned credit less than a value"""
        return [
            {user.uuid: user}
            for user in self._users.values()
            if user.asigned_credits < value
        ]

    def add_user(self, user: User):
        """add a user by company"""
        self._users[user.uuid] = user

    def massive_users_add(self, url, company_uuid):
        """add a massive users by company from a google spreadsheet"""
        data_frame = pd.read_csv(url, encoding='utf8')
        for index, column in data_frame.iterrows():
            self.add_user(
                User(
                    column['first_name'],
                    column['last_name'],
                    f"+ {column['phone_country_code']}{column['phone']}",
                    '',
                    environment('MASSIVE_USER_BY_COMPANY_SECRET_PASSPHRASE'),
                    0.0,
                    company_uuid,
                ),
            )

    def users_export_to_csv(self):
        """exports all users in a csv"""
        data_frame = pd.DataFrame.from_dict(self.users, orient='index')
        data_frame.to_csv(f'template_massive_users_{self.name}.csv')

    def massive_users_update(self, update_url):
        """update a massive users by company from a google spreadsheet"""
        data_frame = pd.read_csv(update_url, encoding='utf8')
        uuid_from_updated_user = []
        # these two for are not necessary, they are part of a proof of concept
        for index, column in data_frame.iterrows():
            for user in self._users.values():
                if user.uuid == column['uuid']:
                    uuid_from_updated_user.append(user.uuid)
                    user.first_name = column['first_name']
                    user.last_name = column['last_name']
                    user.asigned_credits = column['asigned_credits']
                    user.is_active = column['is_active']
        # This return and uuid_from_updated_user is for testeable reasons"""
        # Since the uuid is created at runtime and is an important data reference of the updates"""
        return uuid_from_updated_user

    @property
    def company_representatives(self) -> dict:
        """return a dict of all company representatives by company"""
        return self._company_representatives

    def add_company_representative(self, company_representative: CompanyRepresentative):
        """add a company representatives by company"""
        self._company_representatives[
            company_representative.uuid
        ] = company_representative

    def __str__(self):
        return (
            f'uuid: {self.uuid} name: {self.name} tel: {self.phone} users:{self._users}'
        )
