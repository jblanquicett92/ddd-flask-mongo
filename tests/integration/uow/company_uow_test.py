from __future__ import annotations

import pytest

from src.layers.domain.model.company import Company
from src.layers.persistence.uow.company_uow import CompanyUOW
from src.layers.persistence.utils.company_serializer import CompanySerializer


@pytest.mark.mongomock
def test_company_uow_add_method(mongodb):
    uow = CompanyUOW(session_factory=mongodb)
    uow.company.add(Company('teams', '1010101010'))
    uow.company.add(Company('travel', '200202020'))
    uow.company.add(Company('b2b2c', '3003030'))

    assert len(uow.company.list_all()) == 9


@pytest.mark.mongomock
def test_company_uow_get_method(mongodb):
    uow = CompanyUOW(session_factory=mongodb)
    company_dict_from_mongo_db = uow.company.get({'name': 'organization2.0'})

    assert company_dict_from_mongo_db['name'] == 'organization2.0'
    assert company_dict_from_mongo_db['phone'] == 668015


@pytest.mark.mongomock
def test_company_uow_list_all_method(mongodb):
    uow = CompanyUOW(session_factory=mongodb)

    assert len(uow.company.list_all()) == 6


@pytest.mark.mongomock
def test_company_uow_update_method(mongodb):
    uow = CompanyUOW(session_factory=mongodb)
    company_dict_from_mongo_db = uow.company.get({'name': 'organization2.0'})

    company_serializer = CompanySerializer(company_dict_from_mongo_db)
    company_to_update = company_serializer.company
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    company_to_update._id = company_dict_from_mongo_db['_id']
    company_to_update.phone = '99999991'
    uow.company.update(company_to_update)
    company_dict_from_mongo_db = uow.company.get({'name': 'organization2.0'})
    assert company_dict_from_mongo_db['phone'] == '99999991'
