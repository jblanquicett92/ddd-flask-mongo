from __future__ import annotations

import pytest

from src.layers.domain.model.company_representative import CompanyRepresentative
from src.layers.persistence.uow.company_representative_uow import (
    CompanyRepresentativeUOW,
)
from src.layers.persistence.utils.company_representative_serializer import (
    CompanyRepresentativeSerializer,
)


@pytest.mark.mongomock
def test_company_representative_uow_add_method(mongodb):
    uow = CompanyRepresentativeUOW(session_factory=mongodb)
    uow.company_representative.add(
        CompanyRepresentative(
            'armando', 'matos',
            '+525580158041', 'a.matos@organization.com',
            'helloworld2.0', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    )
    uow.company_representative.add(
        CompanyRepresentative(
            'bbb', 'bbb',
            '+1111111', 'bbb@organization.com',
            'bbbb', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    )
    uow.company_representative.add(
        CompanyRepresentative(
            'bbb', 'bbb',
            '+1111111', 'bbb@organization.com',
            'bbbb', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    )

    assert len(uow.company_representative.list_all()) == 14


@pytest.mark.mongomock
def test_company_representative_uow_get_method_and_serialization(mongodb):
    uow = CompanyRepresentativeUOW(session_factory=mongodb)
    company_representative_dict_from_mongo_db = uow.company_representative.get({'first_name': 'andres'})

    company_representative_serializer = CompanyRepresentativeSerializer(company_representative_dict_from_mongo_db)
    domain_company_representative = company_representative_serializer.company_representative

    assert domain_company_representative.uuid == '221781d0-ad9a-4827-b6a4-929f61c07441'
    assert domain_company_representative.last_name == 'cto'


@pytest.mark.mongomock
def test_company_representative_uow_list_all_method(mongodb):
    uow = CompanyRepresentativeUOW(session_factory=mongodb)

    assert len(uow.company_representative.list_all()) == 11


@pytest.mark.mongomock
def test_company_representative_uow_update_method(mongodb):
    uow = CompanyRepresentativeUOW(session_factory=mongodb)
    company_representative_dict_from_mongo_db = uow.company_representative.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    company_representative_serializer = CompanyRepresentativeSerializer(company_representative_dict_from_mongo_db)
    domain_company_representative_to_update = company_representative_serializer.company_representative
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_company_representative_to_update._id = company_representative_dict_from_mongo_db['_id']
    domain_company_representative_to_update.set_phone_and_code_country('+525580158148')
    domain_company_representative_to_update.first_name = 'RENATO'
    domain_company_representative_to_update.last_name = 'JOAO'

    uow.company_representative.update(domain_company_representative_to_update)
    company_representative_dict_from_mongo_db = uow.company_representative.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    assert company_representative_dict_from_mongo_db['phone'] == 5580158148
    assert company_representative_dict_from_mongo_db['phone_country_code'] == 52
    assert company_representative_dict_from_mongo_db['first_name'] == 'RENATO'
    assert company_representative_dict_from_mongo_db['last_name'] == 'JOAO'


@pytest.mark.mongomock
def test_company_representative_uow_delete_method(mongodb):
    uow = CompanyRepresentativeUOW(session_factory=mongodb)
    company_representative_dict_from_mongo_db = uow.company_representative.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    company_representative_serializer = CompanyRepresentativeSerializer(company_representative_dict_from_mongo_db)
    domain_company_representative_to_delete = company_representative_serializer.company_representative
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_company_representative_to_delete._id = company_representative_dict_from_mongo_db['_id']
    uow.company_representative.delete(domain_company_representative_to_delete)
    assert len(uow.company_representative.list_all()) == 10
