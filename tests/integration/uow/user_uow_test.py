from __future__ import annotations

import pytest

from src.layers.domain.model.user import User
from src.layers.persistence.uow.user_uow import UserUOW
from src.layers.persistence.utils.user_serializer import UserSerializer


@pytest.mark.mongomock
def test_user_uow_add_method(mongodb):
    uow = UserUOW(session_factory=mongodb)
    uow.user.add(
        User(
            'armando', 'matos',
            '+525580158041', 'a.matos@organization.com',
            'helloworld2.0', 12.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    )
    uow.user.add(
        User(
            'bbb', 'bbb',
            '+1111111', 'bbb@organization.com',
            'bbbb', 17.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    )
    uow.user.add(
        User(
            'bbb', 'bbb',
            '+1111111', 'bbb@organization.com',
            'bbbb', 1.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    )

    assert len(uow.user.list_all()) == 20


@pytest.mark.mongomock
def test_user_uow_get_method_and_serialization(mongodb):
    uow = UserUOW(session_factory=mongodb)
    user_dict_from_mongo_db = uow.user.get({'first_name': 'jorge'})

    user_serializer = UserSerializer(user_dict_from_mongo_db)
    domain_user = user_serializer.user

    assert domain_user.uuid == '221781d0-ad9a-4827-b6a4-929f61c07449'
    assert domain_user.first_name == 'jorge'
    assert domain_user.asigned_credits == 50


@pytest.mark.mongomock
def test_user_uow_list_all_method(mongodb):
    uow = UserUOW(session_factory=mongodb)

    assert len(uow.user.list_all()) == 17


@pytest.mark.mongomock
def test_user_uow_update_method(mongodb):
    uow = UserUOW(session_factory=mongodb)
    user_dict_from_mongo_db = uow.user.get({'first_name': 'jorge'})

    user_serializer = UserSerializer(user_dict_from_mongo_db)
    domain_user_to_update = user_serializer.user
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_user_to_update._id = user_dict_from_mongo_db['_id']
    domain_user_to_update.set_phone_and_code_country('+525580158148')
    domain_user_to_update.first_name = 'RENATO'
    domain_user_to_update.last_name = 'JOAO'

    uow.user.update(domain_user_to_update)
    user_dict_from_mongo_db = uow.user.get({'uuid': '221781d0-ad9a-4827-b6a4-929f61c07449'})

    assert user_dict_from_mongo_db['phone'] == 5580158148
    assert user_dict_from_mongo_db['phone_country_code'] == 52
    assert user_dict_from_mongo_db['first_name'] == 'RENATO'
    assert user_dict_from_mongo_db['last_name'] == 'JOAO'


@pytest.mark.mongomock
def test_user_uow_delete_method(mongodb):
    uow = UserUOW(session_factory=mongodb)
    user_dict_from_mongo_db = uow.user.get({'first_name': 'jorge'})

    user_serializer = UserSerializer(user_dict_from_mongo_db)
    domain_user_to_delete = user_serializer.user
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_user_to_delete._id = user_dict_from_mongo_db['_id']
    uow.user.delete(domain_user_to_delete)
    assert len(uow.user.list_all()) == 16
