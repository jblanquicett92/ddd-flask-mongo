from __future__ import annotations

from src.layers.domain.model.account_manager import AccountManager
from src.layers.persistence.uow.account_manager_uow import AccountManagerUOW


class AccountManagerService:
    '''
    RepresentativeService class
    Define functionality on service layer
    '''

    def __init__(self, account_manager_uow: AccountManagerUOW):
        self.account_manager_uow = account_manager_uow

    def add_company_account_manager(self, account_manager: AccountManager):
        '''
        Add Account Manager data to domain model on DB
        function.

        :param account_manager: CompanyRepresentative entity domain model
        '''

        self.account_manager_uow.account_manager.add(account_manager)

    def update_company_account_manager_by_uuid(self, account_manager_updated: AccountManager):
        '''
        Update by UUID attribute Account Manager data to domain model on DB
        function.

        :param account_manager_updated: Company Account Manager object with
                                        data to update
        '''

        self.account_manager_uow.account_manager.update(account_manager_updated)

    def delete_company_account_manager(self, account_manager_deleted: AccountManager):
        '''
        Delete Account Manager data to domain model on DB
        function.

        :param account_manager_deleted: Company Account Manager object with data
                                        to delete
        '''

        self.account_manager_uow.account_manager.delete(account_manager_deleted)

    def get_company_account_manager(self, account_manager_uuid):
        '''
        Retrieve by UUID attribute User Account Manager data from DB
        function.

        :param account_manager_uuid: Company Account Manager UUID with data
                                     to get
        '''

        account_manager_dict_from_mongo_db = self.account_manager_uow.account_manager.get(
            {'uuid': account_manager_uuid},
        )

        return account_manager_dict_from_mongo_db

    def get_company_account_manager_by_name(self, account_manager_name):
        '''
        Retrieve by name attribute Account Manager data from DB
        function.

        :param account_manager_name: Company Account Manager name with data
                                    to get
        '''

        account_manager_dict_from_mongo_db = self.account_manager_uow.account_manager.get(
            {'first_name': account_manager_name},
        )

        return account_manager_dict_from_mongo_db

    def list_all_account_manager(self):
        '''
        Retrieve all Company Account Managers data from DB function
        '''

        account_managers_dict_from_mongo_db = self.account_manager_uow.account_manager.list_all()

        return account_managers_dict_from_mongo_db
