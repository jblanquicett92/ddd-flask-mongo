'''...'''
from __future__ import annotations

from datetime import datetime

from flask_api import status

from src.layers.distribuited_services.bridge.serializer.json.company_schema import CompanySchema
from src.layers.distribuited_services.bridge.serializer.json.user_schema import UserSchema
from src.layers.domain.model.company import Company
from src.layers.services.company_service import CompanyService
from src.layers.services.user_service import UserService


class CompanyRequestHandler:
    '''...'''

    def __init__(self, company_service: CompanyService, user_service: UserService = None) -> None:
        self.company_services = company_service
        self.user_service = user_service
        self.company_schema = CompanySchema()
        self.user_schema = UserSchema()

    # def pagination(self, list_of_companies, sample_range):
    #     '''...'''
    #     return [list_of_companies[i:i + sample_range] for i in range(0, len(list_of_companies), sample_range)]

    # def pagination_response(self, list_of_companies, page):
    #     '''...'''
    #     if page <= 0:
    #         raise Exception('Page cant be zero or negative')
    #     pages = len(list_of_companies)
    #     list_of_companies = list_of_companies[int(page) - 1]
    #     return {'pages': pages, 'results': list_of_companies}

    def number_of_companies(self):
        '''...'''
        try:
            number_of_companies = len(self.company_services.list_all_companies())
            number_of_companies_json = {'size': number_of_companies}
            # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(number_of_companies_json), status.HTTP_200_OK

    def standard_response(self, serialized_data):
        '''...'''
        count = len(serialized_data) if isinstance(serialized_data, list) else 1
        results = serialized_data if count != 1 else [serialized_data]
        
        return {'count': count,
        'errors': [],
        'body': {'results': results}}

    def standard_error_response(self, exception):
        '''...'''
        
        return {'errors': [exception.args[0]]}

    def list_all_companies(self, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.list_all_companies()
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]
        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK

    def list_all_companies_sort_by_name_asc(self, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.list_all_companies()
            list_of_companies.sort(key=lambda company: company.name)
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]
        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK

    def list_all_companies_sort_by_name_desc(self, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.list_all_companies()
            list_of_companies.sort(key=lambda company: company.name, reverse=True)
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]
        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK

    def list_all_companies_sort_by_created_asc(self, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.list_all_companies()
            list_of_companies.sort(
                key=lambda company: datetime.strptime(
                    company.created,
                    '%Y-%m-%d %H:%M:%S.%f',
                ),
            )
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]
        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK

    def list_all_companies_sort_by_created_desc(self, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.list_all_companies()
            list_of_companies.sort(
                key=lambda company: datetime.strptime(
                    company.created,
                    '%Y-%m-%d %H:%M:%S.%f',
                ), reverse=True,
            )
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]
        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK


    def list_all_companies_sort_by_modified_asc(self, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.list_all_companies()
            list_of_companies.sort(
                key=lambda company: datetime.strptime(
                    str(company.modified),
                    '%Y-%m-%d %H:%M:%S.%f',
                ),
            )
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]
        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK

    def list_all_companies_sort_by_modified_desc(self, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.list_all_companies()
            list_of_companies.sort(
                key=lambda company: datetime.strptime(
                    str(company.modified),
                    '%Y-%m-%d %H:%M:%S.%f',
                ), reverse=True,
            )
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]

        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK

    def filter_companies_by_name(self, name, page, showing_range):
        '''...'''
        try:
            list_of_companies = self.company_services.filter_companies_by_name(name)
            list_of_companies = [self.company_schema.dump(company) for company in list_of_companies]
        # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(list_of_companies), status.HTTP_200_OK

    def add_a_company(self, payload):
        '''...'''
        try:
            name, phone, email = payload['name'], payload['phone'], payload['email']
            new_company = Company(
                name,
                phone,
                email,
            )
            domain_company_created = self.company_services.add_company(new_company)
            company_serializated = self.company_schema.dump(domain_company_created)
            
            # pylint: disable=broad-except
        except Exception as exc:
            exception_detail=f'Company model need a {exc.args[0]}'
            return {'errors': ["Attribute on model error", exception_detail]}, status.HTTP_400_BAD_REQUEST
        return self.standard_response(company_serializated), status.HTTP_200_OK

    def get_a_company(self, payload):
        '''Get a company in json format'''
        try:
            uuid = payload['uuid']
            domain_company = self.company_services.get_company(uuid)
            company_serializated = self.company_schema.dump(domain_company)
            # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(company_serializated), status.HTTP_200_OK

    def _update(self, company: Company):
        '''...'''
        try:
            company.modified = str(datetime.now())
            company_updated = self.company_services.update_company(company)
            company_serializated = self.company_schema.dump(company_updated)
        # pylint: disable=broad-except
        except Exception as exc:
            exception_detail=f'Company model need a {exc.args[0]}'
            return {'errors': ["Attribute on model error", exception_detail]}, status.HTTP_400_BAD_REQUEST
        return self.standard_response(company_serializated), status.HTTP_200_OK

    def update_a_company(self, payload):
        '''update contact information'''
        try:
            uuid, name, phone, email = payload['uuid'], payload['name'], payload['phone'], payload['email']
            company_to_update = self.company_services.get_company(uuid)
            company_to_update.name = name
            company_to_update.phone = phone
            company_to_update.email = email
        # pylint: disable=broad-except
        except Exception as exc:
            exception_detail=f'You need to add key-value {exc.args[0]}'
            return {'errors': ["Attribute on model error", exception_detail]}, status.HTTP_400_BAD_REQUEST
        return self._update(company_to_update)

    def active_deactive_company(self, payload):
        '''...'''
        try:
            uuid, is_active = payload['uuid'], payload['is_active']
            company_to_update = self.company_services.get_company(uuid)
            company_to_update.is_active = is_active
        # pylint: disable=broad-except
        except Exception as exc:
            exception_detail=f'You need to add key-value {exc.args[0]}'
            return {'errors': ["Attribute on model error", exception_detail]}, status.HTTP_400_BAD_REQUEST
        return self._update(company_to_update)

    def list_users_by_company(self, payload):
        '''...'''
        domain_company = self.company_services.get_company(payload['uuid'])
        list_users_by_company = self.user_service.list_all_users_by_company(domain_company.uuid)
        list_users_by_company = [self.user_schema.dump(user) for user in list_users_by_company]
        return list_users_by_company

    def number_of_users_by_company(self, payload):
        '''...'''
        domain_company = self.company_services.get_company(payload['uuid'])
        list_users_by_company = self.user_service.list_all_users_by_company(domain_company.uuid)
        return list_users_by_company

    def delete_a_company(self, payload):
        '''Delete a company'''
        try:
            domain_company = self.company_services.get_company(payload['uuid'])
            domain_company_deleted = self.company_services.delete_company(domain_company)
            company_serializated = self.company_schema.dump(domain_company_deleted)
            # pylint: disable=broad-except
        except Exception as exc:
            return self.standard_error_response(exc), status.HTTP_400_BAD_REQUEST
        return self.standard_response(company_serializated), status.HTTP_200_OK
