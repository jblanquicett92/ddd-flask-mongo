from __future__ import annotations

import pytest

from src.layers.domain.model.account_manager import AccountManager
from src.layers.persistence.uow.account_manager_uow import AccountManagerUOW
from src.layers.persistence.utils.account_manager_serializer import (
    AccountManagerSerializer,
)


@pytest.mark.mongomock
def test_account_manager__uow_add_method(mongodb):
    uow = AccountManagerUOW(session_factory=mongodb)
    uow.account_manager.add(
        AccountManager(
            'armando', 'matos',
            '+525580158041', 'a.matos@organization.com',
            'helloworld2.0',
        ),
    )
    uow.account_manager.add(
        AccountManager(
            'bbb', 'bbb',
            '+1111111', 'bbb@organization.com',
            'bbbb',
        ),
    )
    uow.account_manager.add(
        AccountManager(
            'ccc', 'ccc',
            '+22222222', 'ccc@organization.com',
            '222',
        ),
    )

    assert len(uow.account_manager.list_all()) == 4


@pytest.mark.mongomock
def test_account_manager__uow_get_method_and_serialization(mongodb):
    uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_dict_from_mongo_db = uow.account_manager.get({'first_name': 'andres'})

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager_ = account_manager_serializer.account_manager

    assert domain_account_manager_.uuid == '221781d0-ad9a-4827-b6a4-929f61c07441'
    assert domain_account_manager_.last_name == 'cto'


@pytest.mark.mongomock
def test_account_manager_uow_list_all_method(mongodb):
    uow = AccountManagerUOW(session_factory=mongodb)

    assert len(uow.account_manager.list_all()) == 1


@pytest.mark.mongomock
def test_account_manager_uow_update_method(mongodb):
    uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_dict_from_mongo_db = uow.account_manager.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager_to_update = account_manager_serializer.account_manager
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_account_manager_to_update._id = account_manager_dict_from_mongo_db['_id']
    domain_account_manager_to_update.set_phone_and_code_country('+525580158148')
    domain_account_manager_to_update.first_name = 'RENATO'
    domain_account_manager_to_update.last_name = 'JOAO'

    uow.account_manager.update(domain_account_manager_to_update)
    account_manager_dict_from_mongo_db = uow.account_manager.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    assert account_manager_dict_from_mongo_db['phone'] == 5580158148
    assert account_manager_dict_from_mongo_db['phone_country_code'] == 52
    assert account_manager_dict_from_mongo_db['first_name'] == 'RENATO'
    assert account_manager_dict_from_mongo_db['last_name'] == 'JOAO'


@pytest.mark.mongomock
def test_account_manager_uow_delete_method(mongodb):
    uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_dict_from_mongo_db = uow.account_manager.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager_to_delete = account_manager_serializer.account_manager
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_account_manager_to_delete._id = account_manager_dict_from_mongo_db['_id']
    uow.account_manager.delete(domain_account_manager_to_delete)
    assert len(uow.account_manager.list_all()) == 0
