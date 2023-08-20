from __future__ import annotations

import pytest

from src.layers.domain.model.company import Company
from src.layers.persistence.repository.company_repository import CompanyRepository
from src.layers.persistence.utils.company_serializer import CompanySerializer


@pytest.mark.mongomock
def test_company_repository_add_method(mongodb):
    company_repository = CompanyRepository(mongodb)
    testeable_company = Company('b2b', '111222')
    company_repository.add(testeable_company)
    company_dict_from_mongo_db = company_repository.get({'name': 'b2b'})

    assert company_dict_from_mongo_db['name'] == testeable_company.name
    assert company_dict_from_mongo_db['phone'] == testeable_company.phone
    assert company_dict_from_mongo_db['uuid'] == testeable_company.uuid


@pytest.mark.mongomock
def test_company_repository_get_method(mongodb):
    company_repository = CompanyRepository(mongodb)
    company_dict_from_mongo_db = company_repository.get({'name': 'organization2.0'})

    assert company_dict_from_mongo_db['name'] == 'organization2.0'
    assert company_dict_from_mongo_db['phone'] == 668015


@pytest.mark.mongomock
def test_company_repository_list_all_method(mongodb):
    company_repository = CompanyRepository(mongodb)

    assert len(company_repository.list_all()) == 6


@pytest.mark.mongomock
def test_company_repository_update_method(mongodb):
    company_repository = CompanyRepository(mongodb)
    company_dict_from_mongo_db = company_repository.get({'name': 'organization2.0'})

    company_serializer = CompanySerializer(company_dict_from_mongo_db)
    company_to_update = company_serializer.company
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    company_to_update._id = company_dict_from_mongo_db['_id']
    company_to_update.phone = '99999991'
    company_repository.update(company_to_update)
    company_dict_from_mongo_db = company_repository.get({'name': 'organization2.0'})
    assert company_dict_from_mongo_db['phone'] == '99999991'


@pytest.mark.mongomock
def test_company_repository_delete_method(mongodb):
    company_repository = CompanyRepository(mongodb)
    company_dict_from_mongo_db = company_repository.get({'name': 'organization2.0'})

    company_serializer = CompanySerializer(company_dict_from_mongo_db)
    company_to_delete = company_serializer.company
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    company_to_delete._id = company_dict_from_mongo_db['_id']

    company_repository.delete(company_to_delete)
    assert len(company_repository.list_all()) == 5
