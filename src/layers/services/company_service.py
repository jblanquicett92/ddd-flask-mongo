'''Define functionality on service layer'''
from __future__ import annotations

from src.layers.domain.model.company import Company
from src.layers.persistence.uow.company_uow import CompanyUOW
from src.layers.persistence.utils.company_serializer import CompanySerializer
from src.layers.services.exceptions import AttributeUUIDNotExists
from src.layers.services.exceptions import UUIDIsAsignedInAthotherCompany
from src.layers.services.integration.external.sync.rpc_ms_tower import create_company
from src.layers.services.integration.external.sync.rpc_ms_tower import get_token
from src.layers.services.integration.external.sync.rpc_ms_tower import login


class CompanyService:
    '''
    CompanyService class
    Define functionality on service layer
    '''

    def __init__(self, company_uow: CompanyUOW):
        self.company_uow = company_uow

    def login_and_get_token(self):
        response = login()
        token = get_token(response)
        return token

    def notify_add_company(self, company):
        '''
        Notify all legacy and pre-legacy when a company its created
        '''
        token = self.login_and_get_token()
        create_company(token, company)

    def add_company(self, company: Company):
        '''
        Add Company data to domain model on DB
        function.

        :param company: Company entity domain model
        '''

        if (self.company_uow.company.get({'uuid': company.uuid})) is None:
            self.notify_add_company(company)
            self.company_uow.company.add(company)
            return company
        raise UUIDIsAsignedInAthotherCompany('UUID is already assigned in another company')

    def update_company(self, company_to_update: Company):
        '''
        Update by UUID attribute User data to domain model on DB
        function.

        :param company_to_update: Company object with
                                       data to update
        '''

        self.company_uow.company.update(company_to_update)
        return company_to_update

    def delete_company(self, company_to_delete: Company):
        '''
        Delete Company data to domain model on DB
        function.

        :param company_to_delete: Company object with data to delete
        '''
        if (self.company_uow.company.get({'uuid': company_to_delete.uuid})) is not None:
            self.company_uow.company.delete(company_to_delete)
            return company_to_delete
        raise AttributeUUIDNotExists('UUID is not assigned in another company in the data store')

    def get_company(self, uuid: str):
        '''
        Retrieve by UUID attribute User data from DB
        function.

        :param company_uuid: Company dictionary with data
                             to update
        '''

        company_dict_from_mongo_db = self.company_uow.company.get({'uuid': uuid})
        if company_dict_from_mongo_db is None:
            raise AttributeUUIDNotExists('UUID is not exist')
        company_serializer = CompanySerializer(company_dict_from_mongo_db)
        domain_company = company_serializer.company
        return domain_company

    def get_company_by_name(self, company: Company) -> Company:
        '''
        Retrieve by name attribute User data from DB
        function.

        :param company_name: Company dictionary with data
                             to update
        '''

        company_dict_from_mongo_db = self.company_uow.company.get({'name': company.name})
        company_serializer = CompanySerializer(company_dict_from_mongo_db)
        domain_company = company_serializer.company

        return domain_company

    def list_all_companies(self):
        '''
        Retrieve all Companies data from DB function
        '''

        companies_from_mongo_db = self.company_uow.company.list_all()

        return [CompanySerializer(company_mongo).company for company_mongo in companies_from_mongo_db]

    def filter_companies_by_name(self, name: str):
        '''
        Retrieve all Companies data from DB function
        '''

        companies_from_mongo_db = self.company_uow.company.filter_by_name(name)

        return [CompanySerializer(company_mongo).company for company_mongo in companies_from_mongo_db]
