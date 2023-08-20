"""This file has the purpose of test users in json format"""
from __future__ import annotations

from src.layers.distribuited_services.bridge.serializer.json.user_schema import (
    UserSchema,
)
from src.layers.distribuited_services.bridge.utils.formatter import is_json, json
from src.layers.domain.model.user import User


def make_users():
    """Fixture will generate users in memory"""
    return [
        User(
            'jorge', 'blanquicett',
            '+525580158040', 'j.blanquicett@organization.com',
            'helloworld', 50.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
        User(
            'armando', 'matos',
            '+525580158041', 'a.matos@organization.com',
            'helloworld2.0', 50.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    ]


def test_user_in_json_format():
    """assert when a company has json format"""
    testeable_user = make_users()[0]  # In Prod env, please remove this little line for a uow.user.find({})
    user_json_schema = UserSchema()
    user_serializated = user_json_schema.dump(testeable_user)
    user_json = json.dumps(user_serializated, indent=2)

    assert is_json(user_json) is True


def test_list_of_users_in_json_format():
    """assert when a list of companies has json format"""

    user_json_schema = UserSchema()
    testeable_users = make_users()  # In Prod env, please remove this little line for a uow.user.list() or similar
    list_of_users = [user_json_schema.dump(company) for company in testeable_users]
    list_of_users_in_json_format = json.dumps(list_of_users, indent=2)

    assert is_json(list_of_users_in_json_format) is True
    assert len(testeable_users) == 2
