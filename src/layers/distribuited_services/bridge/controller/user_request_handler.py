'''...'''
from __future__ import annotations

from datetime import datetime

from src.layers.distribuited_services.bridge.serializer.json.user_schema import UserSchema
from src.layers.distribuited_services.bridge.utils.formatter import json
from src.layers.domain.model.user import User
from src.layers.services.user_service import UserService


class UserRequestHandler:
    '''...'''

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service
        self.user_schema = UserSchema()

    def number_of_users(self):
        '''...'''
        number_of_users = len(self.user_service.list_all_users())
        number_of_users_json = json.dumps({'number_of_users': number_of_users})
        return number_of_users_json

    def list_all_users(self):
        '''...'''
        # list[User]
        list_of_users = self.user_service.list_all_users()
        # list[{'..':'..', '..':'..'}]
        list_of_users = [self.user_schema.dump(company) for company in list_of_users]
        # '[{'..':'..', '..':'..'}]'
        list_of_users = json.dumps(list_of_users)
        return list_of_users

    def add_a_user(self, payload):
        '''...'''
        first_name, last_name = payload['first_name'], payload['last_name']
        phone, email = payload['phone'], payload['email']
        password, asigned_credits = payload['password'], payload['asigned_credits']
        company_uuid = payload['company_uuid']

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            _email=email,
            password=password,
            asigned_credits=asigned_credits,
            company_uuid=company_uuid,
        )
        self.user_service.add_user(new_user)
        user_serializated = self.user_schema.dump(new_user)
        user_serializated = json.dumps(user_serializated)
        return user_serializated

    def get_a_user(self, payload):
        '''...'''
        uuid = payload['uuid']
        domain_user = self.user_service.get_user(uuid)
        user_serializated = self.user_schema.dump(domain_user)
        user_serializated = json.dumps(user_serializated)
        return user_serializated

    def _update(self, user: User):
        '''...'''
        user.modified = datetime.now()
        user_updated = self.user_service.update_user(user)
        user_serializated = self.user_schema.dump(user_updated)
        user_serializated = json.dumps(user_serializated)
        return user_serializated

    def update_contact_info_for_a_user(self, payload):
        '''...'''
        first_name, last_name = payload['first_name'], payload['last_name']
        phone, email = payload['phone'], payload['email']
        uuid = payload['uuid']

        user_to_update = self.user_service.get_user(uuid)
        user_to_update.email = email
        user_to_update.first_name = first_name
        user_to_update.last_name = last_name
        user_to_update.set_phone_and_code_country(phone)

        return self._update(user_to_update)

    def update_asigned_credits(self, payload):
        '''...'''
        company_uuid, asigned_credits = payload['company_uuid'], payload['asigned_credits']

        user_to_update = self.user_service.get_user(company_uuid)
        user_to_update.asigned_credits = asigned_credits

        return self._update(user_to_update)

    def list_users(self):
        '''...'''
        list_users = self.user_service.list_all_users()
        # list[{'..':'..', '..':'..'}]
        list_users = [self.user_schema.dump(user) for user in list_users]
        # '[{'..':'..', '..':'..'}]'
        list_users = json.dumps(list_users)
        return list_users
