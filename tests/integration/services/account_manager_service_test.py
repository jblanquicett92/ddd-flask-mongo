from __future__ import annotations

import pytest

from src.layers.domain.model.account_manager import AccountManager
from src.layers.persistence.uow.account_manager_uow import AccountManagerUOW
from src.layers.persistence.utils.account_manager_serializer import (
    AccountManagerSerializer,
)
from src.layers.services.account_manager_service import AccountManagerService
from src.layers.services.exceptions import AttributeUUIDNotExists


def make_account_manager_users():
    return [
        AccountManager(
            'armando', 'matos',
            '+525580158041', 'a.matos@organization.com',
            'helloworld2.0',
        ),
        AccountManager(
            'bbb', 'bbb',
            '+1111111', 'bbb@organization.com',
            'bbbb',
        ),
        AccountManager(
            'ccc', 'ccc',
            '+22222222', 'ccc@organization.com',
            '222',
        ),
    ]


@pytest.mark.mongomock
def test_add_account_manager_service(mongodb):
    account_manager_uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_service = AccountManagerService(account_manager_uow=account_manager_uow)

    data_from_mongo_db = account_manager_service.list_all_account_manager()

    for user_am in make_account_manager_users():
        account_manager_service.add_company_account_manager(user_am)

        for account_user in data_from_mongo_db:
            account_manager_serializer = AccountManagerSerializer(account_user)
            domain_account_manager = account_manager_serializer.account_manager

            assert domain_account_manager.uuid != user_am.uuid

    assert len(account_manager_uow.account_manager.list_all()) == 4


@pytest.mark.mongomock
def test_get_by_name_account_manager_service(mongodb):
    account_manager_uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_service = AccountManagerService(account_manager_uow=account_manager_uow)

    account_manager_name_param = 'andres'

    account_manager_dict_from_mongo_db = account_manager_service.get_company_account_manager_by_name(
        account_manager_name_param,
    )

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager = account_manager_serializer.account_manager

    try:
        if hasattr(domain_account_manager, 'uuid'):
            assert domain_account_manager.uuid == '221781d0-ad9a-4827-b6a4-929f61c07441'
            assert domain_account_manager.last_name == 'cto'

    except AttributeUUIDNotExists as exc:
        assert exc.args[0] == 'UUID Account Manager User Domain Object does not exists'


@pytest.mark.mongomock
def test_list_account_manager_service(mongodb):
    account_manager_uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_service = AccountManagerService(account_manager_uow=account_manager_uow)

    data_from_mongo_db = account_manager_service.list_all_account_manager()

    assert len(data_from_mongo_db) >= 1


@pytest.mark.mongomock
def test_update_account_manager_service(mongodb):
    account_manager_uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_service = AccountManagerService(account_manager_uow=account_manager_uow)

    account_manager_uuid_param = '221781d0-ad9a-4827-b6a4-929f61c07441'

    account_manager_dict_from_mongo_db = account_manager_service.get_company_account_manager(
        account_manager_uuid_param,
    )

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager_to_update = account_manager_serializer.account_manager

    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_account_manager_to_update._id = account_manager_dict_from_mongo_db['_id']
    domain_account_manager_to_update.set_phone_and_code_country('+525580158148')
    domain_account_manager_to_update.first_name = 'Renato'
    domain_account_manager_to_update.last_name = 'Piccard'

    try:
        if hasattr(domain_account_manager_to_update, 'uuid'):

            account_manager_service.update_company_account_manager_by_uuid(domain_account_manager_to_update)

    except AttributeUUIDNotExists as exc:
        assert exc.args[0] == 'UUID Account Manager User Domain Object does not exists'

    account_manager_name_param = 'Renato'

    account_manager_dict_from_mongo_db_updated = account_manager_service.get_company_account_manager_by_name(
        account_manager_name_param,
    )

    account_manager_updated_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db_updated)
    domain_account_manager_updated = account_manager_updated_serializer.account_manager

    assert domain_account_manager_updated.phone == domain_account_manager_to_update.phone
    assert domain_account_manager_updated.phone_country_code == domain_account_manager_to_update.phone_country_code
    assert domain_account_manager_updated.first_name == domain_account_manager_to_update.first_name
    assert domain_account_manager_updated.last_name == domain_account_manager_to_update.last_name


@pytest.mark.mongomock
def test_delete_account_manager_service(mongodb):
    account_manager_uow = AccountManagerUOW(session_factory=mongodb)
    account_manager_service = AccountManagerService(account_manager_uow=account_manager_uow)

    account_manager_name_param = 'andres'

    account_manager_dict_from_mongo_db = account_manager_service.get_company_account_manager_by_name(
        account_manager_name_param,
    )

    account_manager_serializer = AccountManagerSerializer(account_manager_dict_from_mongo_db)
    domain_account_manager_to_delete = account_manager_serializer.account_manager

    try:
        if hasattr(domain_account_manager_to_delete, 'uuid'):
            # in a normal case this assignment would not make sense, but at the time of creating this test
            # I didn't know how to create an objectid in yaml
            domain_account_manager_to_delete._id = account_manager_dict_from_mongo_db.get('_id')

            account_manager_service.delete_company_account_manager(domain_account_manager_to_delete)

    except AttributeUUIDNotExists as exc:
        assert exc.args[0] == 'UUID Company Domain Object does not exists'
