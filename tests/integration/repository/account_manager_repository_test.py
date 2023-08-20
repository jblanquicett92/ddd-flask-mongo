from __future__ import annotations

import pytest

from src.layers.domain.model.account_manager import AccountManager
from src.layers.persistence.repository.account_manager_repository import (
    AccountManagerRepository,
)
from src.layers.persistence.utils.account_manager_serializer import (
    AccountManagerSerializer,
)


@pytest.mark.mongomock
def test_account_manager_repository_add_method(mongodb):
    testeable_account_manager = AccountManager(
        'armando', 'matos',
        '+525580158041', 'a.matos@organization.com',
        'helloworld2.0',
    )
    account_manager_repository = AccountManagerRepository(mongodb)
    account_manager_repository.add(testeable_account_manager)
    account_manager_dict_from_mongo_db = account_manager_repository.get({'first_name': 'armando'})

    assert account_manager_dict_from_mongo_db['uuid'] == testeable_account_manager.uuid
    assert account_manager_dict_from_mongo_db['first_name'] == testeable_account_manager.first_name
    assert account_manager_dict_from_mongo_db['phone'] == testeable_account_manager.phone


@pytest.mark.mongomock
def test_account_manager_repository_get_method_and_serialization(mongodb):
    account_manager_repository = AccountManagerRepository(mongodb)
    account_manager_dict_from_mongo_db = account_manager_repository.get({'last_name': 'cto'})

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager = account_manager_serializer.account_manager

    assert domain_account_manager.uuid == '221781d0-ad9a-4827-b6a4-929f61c07441'
    assert domain_account_manager.first_name == 'andres'


@pytest.mark.mongomock
def test_account_manager_repository_list_all_method(mongodb):
    account_manager_repository = AccountManagerRepository(mongodb)
    assert len(account_manager_repository.list_all()) == 1


@pytest.mark.mongomock
def test_account_manager_repository_update_method(mongodb):
    account_manager_repository = AccountManagerRepository(mongodb)
    account_manager_dict_from_mongo_db = account_manager_repository.get({'last_name': 'cto'})

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager_to_update = account_manager_serializer.account_manager
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_account_manager_to_update._id = account_manager_dict_from_mongo_db['_id']

    domain_account_manager_to_update.set_phone_and_code_country('+525580158148')
    domain_account_manager_to_update.first_name = 'LUISITO'
    domain_account_manager_to_update.last_name = 'MORFINEZ'

    account_manager_repository.update(domain_account_manager_to_update)
    account_manager_dict_from_mongo_db = account_manager_repository.get(
        {'uuid': '221781d0-ad9a-4827-b6a4-929f61c07441'},
    )

    assert account_manager_dict_from_mongo_db['phone_country_code'] == 52
    assert account_manager_dict_from_mongo_db['first_name'] == 'LUISITO'
    assert account_manager_dict_from_mongo_db['last_name'] == 'MORFINEZ'


@pytest.mark.mongomock
def test_account_manager_repository_delete_method(mongodb):
    account_manager_repository = AccountManagerRepository(mongodb)
    account_manager_dict_from_mongo_db = account_manager_repository.get({'last_name': 'cto'})

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager_to_delete = account_manager_serializer.account_manager
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_account_manager_to_delete._id = account_manager_dict_from_mongo_db['_id']

    account_manager_repository.delete(domain_account_manager_to_delete)
    assert len(account_manager_repository.list_all()) == 0
