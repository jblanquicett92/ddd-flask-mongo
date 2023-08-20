'''This test file has the intention ...'''
from __future__ import annotations

import pytest

from src.layers.domain.model.company import Company
from src.layers.persistence.uow.company_uow import CompanyUOW
from src.layers.services.company_service import CompanyService


@pytest.mark.mongomock
def test_company_service_add_a_company(mongodb):
    '''assert when services add a company correctly'''

    company_service = CompanyService(CompanyUOW(mongodb))

    assert len(company_service.list_all_companies()) == 6

    domain_company = Company('amazonia', '10100101')
    company_service.add_company(domain_company)

    assert len(company_service.list_all_companies()) == 7


@pytest.mark.mongomock
def test_company_service_get_a_company(mongodb):
    '''assert when services get a company correctly'''

    company_service = CompanyService(CompanyUOW(mongodb))

    uuid = 'ddc65e81-3439-4edd-a6d8-27808187b0fa'
    company_from_services = company_service.get_company(uuid)

    assert company_from_services.uuid == uuid
    assert company_from_services.name == 'organization3.0'
    assert company_from_services.phone == 668115


@pytest.mark.mongomock
def test_company_service_update_a_company(mongodb):
    '''assert when services update a company correctly'''

    company_service = CompanyService(CompanyUOW(mongodb))

    uuid = 'ddc65e81-3439-4edd-a6d8-27808187b0fa'
    company_to_update = company_service.get_company(uuid)

    company_to_update.name = 'ñamñam'
    company_to_update.phone = 999999

    company_service.update_company(company_to_update)
    company_updated = company_service.get_company(uuid)

    assert company_updated.uuid == uuid
    assert company_updated.name == 'ñamñam'
    assert company_updated.phone == 999999


@pytest.mark.mongomock
def test_company_service_delete_a_company(mongodb):
    '''assert when services delete a company correctly'''

    company_service = CompanyService(CompanyUOW(mongodb))

    uuid = 'ddc65e81-3439-4edd-a6d8-27808187b0fa'
    company_to_delete = company_service.get_company(uuid)

    assert len(company_service.list_all_companies()) == 6
    company_service.delete_company(company_to_delete)
    assert len(company_service.list_all_companies()) == 5


@pytest.mark.mongomock
def test_company_service_list_companies(mongodb):
    '''assert when services list all the companies correctly'''
    company_service = CompanyService(CompanyUOW(mongodb))
    assert all(isinstance(domain_company, Company) for domain_company in company_service.list_all_companies())
    assert len(company_service.list_all_companies()) == 6
