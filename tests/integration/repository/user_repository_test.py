from __future__ import annotations

import pytest

from src.layers.domain.model.user import User
from src.layers.persistence.repository.user_repository import UserRepository
from src.layers.persistence.utils.user_serializer import UserSerializer


@pytest.mark.mongomock
def test_user_repository_add_method(mongodb):
    testeable_user = User(
        'armando', 'matos',
        '+525580158041', 'a.matitos@organization.com',
        'helloworld2.0', 50.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
    )
    user_repository = UserRepository(mongodb)
    user_repository.add(testeable_user)
    user_dict_from_mongo_db = user_repository.get({'_email': 'a.matitos@organization.com'})

    assert user_dict_from_mongo_db['uuid'] == testeable_user.uuid
    assert user_dict_from_mongo_db['first_name'] == testeable_user.first_name
    assert user_dict_from_mongo_db['phone'] == testeable_user.phone
    assert user_dict_from_mongo_db['asigned_credits'] == testeable_user.asigned_credits


@pytest.mark.mongomock
def test_user_repository_get_method_and_serialization(mongodb):
    user_repository = UserRepository(mongodb)
    user_dict_from_mongo_db = user_repository.get({'last_name': 'blanquicett'})

    user_serializer = UserSerializer(user_dict_from_mongo_db)
    domain_user = user_serializer.user

    assert domain_user.uuid == '221781d0-ad9a-4827-b6a4-929f61c07449'
    assert domain_user.first_name == 'jorge'
    assert domain_user.asigned_credits == 50


@pytest.mark.mongomock
def test_user_repository_list_all_method(mongodb):
    user_repository = UserRepository(mongodb)
    assert len(user_repository.list_all()) == 17


@pytest.mark.mongomock
def test_user_repository_update_method(mongodb):
    user_repository = UserRepository(mongodb)
    user_dict_from_mongo_db = user_repository.get({'last_name': 'blanquicett'})

    user_serializer = UserSerializer(user_dict_from_mongo_db)
    domain_user_to_update = user_serializer.user
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_user_to_update._id = user_dict_from_mongo_db['_id']

    domain_user_to_update.set_phone_and_code_country('+525580158148')
    domain_user_to_update.first_name = 'RENATO'
    domain_user_to_update.last_name = 'JOAO'

    user_repository.update(domain_user_to_update)
    user_dict_from_mongo_db = user_repository.get({'uuid': '221781d0-ad9a-4827-b6a4-929f61c07449'})

    assert user_dict_from_mongo_db['phone'] == 5580158148
    assert user_dict_from_mongo_db['phone_country_code'] == 52
    assert user_dict_from_mongo_db['first_name'] == 'RENATO'
    assert user_dict_from_mongo_db['last_name'] == 'JOAO'


@pytest.mark.mongomock
def test_user_repository_delete_method(mongodb):
    user_repository = UserRepository(mongodb)
    user_dict_from_mongo_db = user_repository.get({'last_name': 'blanquicett'})

    user_serializer = UserSerializer(user_dict_from_mongo_db)
    domain_user_to_delete = user_serializer.user
    # in a normal case this assignment would not make sense, but at the time of creating this test
    # I didn't know how to create an objectid in yaml
    domain_user_to_delete._id = user_dict_from_mongo_db['_id']

    user_repository.delete(domain_user_to_delete)
    assert len(user_repository.list_all()) == 16
