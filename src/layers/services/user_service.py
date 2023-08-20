'''Define functionality on service layer'''
from __future__ import annotations

from src.layers.domain.model.user import User
from src.layers.persistence.uow.user_uow import UserUOW
from src.layers.persistence.utils.user_serializer import UserSerializer


class UserService:
    '''
    UserService class
    Define functionality on service layer
    '''

    def __init__(self, user_uow: UserUOW):
        self.user_uow = user_uow

    def add_user(self, user: User):
        '''
        Add User data to domain model on DB
        function.

        :param user: User entity domain model
        '''

        self.user_uow.user.add(user)
        return user

    def update_user(self, user_to_update: User):
        '''
        Update by UUID attribute User data to domain model on DB
        function.

        :param user_to_update: User object with data to update
        '''

        self.user_uow.user.update(user_to_update)
        return user_to_update

    def delete_user(self, user_to_delete: User):
        '''
        Delete User data to domain model on DB
        function.

        :param user_to_delete: User object with data to delete
        '''

        self.user_uow.user.delete(user_to_delete)
        return user_to_delete

    def get_user(self, user_uuid):
        '''
        Retrieve by UUID attribute User data from DB
        function.

        :param user_uuid: User dictionary with data
                          to update
        '''

        user_dict_from_mongo_db = self.user_uow.user.get({'uuid': user_uuid})
        user_serializer = UserSerializer(user_dict_from_mongo_db)
        domain_user = user_serializer.user

        return domain_user

    def list_all_users(self):
        '''
        Retrieve all Users data from DB function
        '''

        users_from_mongo_db = self.user_uow.user.list_all()

        return [UserSerializer(user_in_dict_format).user for user_in_dict_format in users_from_mongo_db]

    def list_all_users_by_company(self, company_uuid):
        '''
        Retrieve all Users data from DB function
        '''

        users_from_mongo_db = self.user_uow.user.list_all_compound_by(company_uuid)

        return [UserSerializer(user_in_dict_format).user for user_in_dict_format in users_from_mongo_db]
