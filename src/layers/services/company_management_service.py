from __future__ import annotations

from src.layers.domain.model.company import pd
from src.layers.services.company_service import CompanyService
from src.layers.services.user_service import UserService


class CompanyManagementService:
    '''...'''

    def __init__(self, company_service: CompanyService, user_service: UserService) -> None:

        self.company_service = company_service
        self.user_service = user_service
        self.google_sheet_pool = None

    # TO-DO: Its not necesary to have this method, use custom utilities to regex google sheet
    def pool_connection_google_sheet(self, sheet_id, sheet_name):
        '''template for google_spreadsheets'''
        goole_sheet_url = 'https://docs.google.com/spreadsheets/d/'
        sheet_gviz = '/gviz/tq?tqx=out:csv&sheet='
        self.google_sheet_pool = f'{goole_sheet_url}{sheet_id}{sheet_gviz}{sheet_name}'
        return self.google_sheet_pool

    def massive_users_create(self, company_uuid):
        '''...'''
        domain_company = self.company_service.get_company(company_uuid)
        domain_company.massive_users_add(self.google_sheet_pool, domain_company.uuid)
        # pylint: disable=protected-access
        for user in domain_company._users.values():  # TO-DO: Improve this
            self.user_service.add_user(user)
        return len(domain_company._users)

    def massive_users_update(self, company_uuid):
        '''...'''
        number_of_users_updated = 0

        domain_company = self.company_service.get_company(company_uuid)

        data_frame = pd.read_csv(self.google_sheet_pool, encoding='utf8')

        for index, column in data_frame.iterrows():
            domain_user = self.user_service.get_user(column['uuid'])
            if domain_user.company_uuid != domain_company.uuid:
                raise Exception('User is not from the company')
            domain_user.first_name = column['first_name']
            domain_user.last_name = column['last_name']
            domain_user.email = column['email']
            domain_user.phone_country_code = column['phone_country_code']
            domain_user.phone = column['phone']
            domain_user.asigned_credits = column['asigned_credits']
            domain_user.is_active = column['is_active']
            self.user_service.update_user(domain_user)
            number_of_users_updated += 1
        return number_of_users_updated
