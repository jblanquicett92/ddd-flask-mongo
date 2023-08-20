from __future__ import annotations

import pytest

from src.layers.domain.model.user import User
from src.layers.persistence.uow.company_uow import CompanyUOW
from src.layers.persistence.uow.user_uow import UserUOW
from src.layers.services.company_management_service import CompanyManagementService
from src.layers.services.company_service import CompanyService
from src.layers.services.user_service import UserService


def connection_pool_to_google_spreadsheets(sheet_id: str, sheet_name: str):
    '''template for google_spreadsheets'''
    return f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


@pytest.mark.mongomock
def test_massive_users_create(mongodb):
    '''...'''

    user_service = UserService(UserUOW(mongodb))
    company_services = CompanyService(CompanyUOW(mongodb))
    company_management_services = CompanyManagementService(company_services, user_service)

    company_management_services.pool_connection_google_sheet(
        '1mbyk0OfajYo2owwcmVTXuVGIIVeHj4eINZldPiSNNoU',
        'template_create_massive_users',
    )
    companies_added = company_management_services.massive_users_create('ddc65e81-3439-4edd-a6d8-27808187b0fa')

    assert companies_added == 7
    assert all(isinstance(domain_user, User) for domain_user in user_service.list_all_users())


@pytest.mark.mongomock
def test_massive_users_update(mongodb):
    '''...'''

    user_service = UserService(UserUOW(mongodb))
    company_services = CompanyService(CompanyUOW(mongodb))
    company_management_services = CompanyManagementService(company_services, user_service)

    company_management_services.pool_connection_google_sheet(
        '1gi9ZqcFITY91npJvdaMQJTBp2GNCxoVUXu-_S8HXqXQ',
        'template_massive_users_update',
    )

    companies_updated = company_management_services.massive_users_update('ddc65e81-3439-4edd-a6d8-27808187b0fa')
    assert companies_updated == 1

    domain_user_updated = user_service.get_user('221781d0-ad9a-4827-b6a4-929f61c07449')

    assert domain_user_updated.first_name == 'xixixi'
    assert domain_user_updated.last_name == 'yoyoyo'
    assert domain_user_updated.email == 'ttt@organization.com'
    assert domain_user_updated.phone_country_code == 52
    assert domain_user_updated.phone == 9991111
    assert domain_user_updated.asigned_credits == 1250
    assert domain_user_updated.is_active is True

    assert all(isinstance(domain_user, User) for domain_user in user_service.list_all_users())
