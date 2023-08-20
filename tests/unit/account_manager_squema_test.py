"""This file has the purpose of test accounts managers in json format"""
from __future__ import annotations

from src.layers.distribuited_services.bridge.serializer.json.account_manager_schema import (
    AccountManagerSchema,
)
from src.layers.distribuited_services.bridge.utils.formatter import is_json, json
from src.layers.domain.model.account_manager import AccountManager


def make_account_managers():
    """Fixture will generate account managers in memory"""
    return [
        AccountManager(
            'jorge', 'blanquicett',
            '+525580158040', 'j.blanquicett@organization.com',
            'helloworld',
        ),
        AccountManager(
            'armando', 'matos',
            '+525580158041', 'a.matos@organization.com',
            'helloworld2.0',
        ),
    ]


def test_account_manager_in_json_format():
    """assert when a company has json format"""
    testeable_account_manager = make_account_managers(
    )[0]  # In Prod env, please remove this little line for a uow.account_manager.find({})
    account_manager_json_schema = AccountManagerSchema()
    account_manager_serializated = account_manager_json_schema.dump(testeable_account_manager)
    account_manager_json = json.dumps(account_manager_serializated, indent=2)

    assert is_json(account_manager_json) is True


def test_list_of_account_managers_in_json_format():
    """assert when a list of companies has json format"""

    account_manager_json_schema = AccountManagerSchema()
    # In Prod env, please remove this little line for a uow.account_manager.list() or similar
    testeable_account_managers = make_account_managers()
    list_of_account_managers = [
        account_manager_json_schema.dump(
            company,
        ) for company in testeable_account_managers
    ]
    list_of_account_managers_in_json_format = json.dumps(list_of_account_managers, indent=2)

    assert is_json(list_of_account_managers_in_json_format) is True
    assert len(testeable_account_managers) == 2
