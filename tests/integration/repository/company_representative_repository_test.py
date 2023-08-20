from __future__ import annotations

import pytest

from src.layers.domain.model.company_representative import CompanyRepresentative
from src.layers.persistence.repository.company_representative_repository import (
    CompanyRepresentativeRepository,
)
from src.layers.persistence.utils.company_representative_serializer import (
    CompanyRepresentativeSerializer,
)


@pytest.mark.mongomock
def test_company_representative_repository_add_method(mongodb):
    testeable_company_representative = CompanyRepresentative(
        'armando', 'matos',
        '+525580158041', 'a.matos@organization.com',
        'helloworld2.0', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
    )
    company_representative_repository = CompanyRepresentativeRepository(mongodb)
    company_representative_repository.add(testeable_company_representative)
    company_representative_dict_from_mongo_db = company_representative_repository.get({'first_name': 'armando'})

    assert company_representative_dict_from_mongo_db['uuid'] == testeable_company_representative.uuid
    assert company_representative_dict_from_mongo_db['first_name'] == testeable_company_representative.first_name
    assert company_representative_dict_from_mongo_db['phone'] == testeable_company_representative.phone


@pytest.mark.mongomock
def test_company_representative_repository_get_method_and_serialization(mongodb):
    company_representative_repository = CompanyRepresentativeRepository(mongodb)
    company_representative_dict_from_mongo_db = company_representative_repository.get({'last_name': 'cto'})

    company_representative_serializer = CompanyRepresentativeSerializer(company_representative_dict_from_mongo_db)
    domain_company_representative = company_representative_serializer.company_representative

    assert domain_company_representative.uuid == '221781d0-ad9a-4827-b6a4-929f61c07441'
    assert domain_company_representative.first_name == 'andres'


@pytest.mark.mongomock
def test_company_representative_repository_list_all_method(mongodb):
    company_representative_repository = CompanyRepresentativeRepository(mongodb)
    assert len(company_representative_repository.list_all()) == 11


@pytest.mark.mongomock
def test_company_representative_repository_update_method(mongodb):
    company_representative_repository = CompanyRepresentativeRepository(mongodb)
    company_representative_dict_from_mongo_db = company_representative_repository.get({'last_name': 'cto'})

    company_representative_serializer = CompanyRepresentativeSerializer(company_representative_dict_from_mongo_db)
    domain_company_representative_to_update = company_representative_serializer.company_representative
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_company_representative_to_update._id = company_representative_dict_from_mongo_db['_id']

    domain_company_representative_to_update.set_phone_and_code_country('+525580158148')
    domain_company_representative_to_update.first_name = 'LUISITO'
    domain_company_representative_to_update.last_name = 'MORFINEZ'

    company_representative_repository.update(domain_company_representative_to_update)
    company_representative_dict_from_mongo_db = company_representative_repository.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    assert company_representative_dict_from_mongo_db['phone_country_code'] == 52
    assert company_representative_dict_from_mongo_db['first_name'] == 'LUISITO'
    assert company_representative_dict_from_mongo_db['last_name'] == 'MORFINEZ'


@pytest.mark.mongomock
def test_company_representative_repository_delete_method(mongodb):
    company_representative_repository = CompanyRepresentativeRepository(mongodb)
    company_representative_dict_from_mongo_db = company_representative_repository.get({'last_name': 'cto'})

    company_representative_serializer = CompanyRepresentativeSerializer(company_representative_dict_from_mongo_db)
    domain_company_representative_to_delete = company_representative_serializer.company_representative
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_company_representative_to_delete._id = company_representative_dict_from_mongo_db['_id']

    company_representative_repository.delete(domain_company_representative_to_delete)
    assert len(company_representative_repository.list_all()) == 10
