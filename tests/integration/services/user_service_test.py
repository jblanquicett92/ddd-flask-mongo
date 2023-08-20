from __future__ import annotations

import pytest

from src.layers.domain.model.user import User
from src.layers.persistence.uow.user_uow import UserUOW
from src.layers.services.user_service import UserService


@pytest.mark.mongomock
def test_user_service_add_an_user(mongodb):
    '''assert when services add a company correctly'''
    user_service = UserService(UserUOW(mongodb))
    assert len(user_service.list_all_users()) == 17

    domain_user = User(
        'armando', 'matos',
        '+525580158041', 'a.matos@organization.com',
        'helloworld2.0', 50.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
    )

    user_service.add_user(domain_user)
    assert len(user_service.list_all_users()) == 18


@pytest.mark.mongomock
def test_user_service_get_an_user(mongodb):
    '''assert when services get a user correctly'''

    user_service = UserService(UserUOW(mongodb))

    uuid = '221781d0-ad9a-4827-b6a4-929f61c07449'
    domain_user_from_services = user_service.get_user(uuid)

    assert domain_user_from_services.first_name == 'jorge'
    assert domain_user_from_services.last_name == 'blanquicett'
    assert domain_user_from_services.username == 'jblanquicett221781d0'


@pytest.mark.mongomock
def test_user_service_update_an_user(mongodb):
    '''assert when services update a user correctly'''

    user_service = UserService(UserUOW(mongodb))

    uuid = '221781d0-ad9a-4827-b6a4-929f61c07449'
    domain_user_to_update = user_service.get_user(uuid)

    domain_user_to_update.first_name = 'XXXX'
    domain_user_to_update.last_name = 'ZZZZ'
    domain_user_to_update.username = 'YYYY'

    user_service.update_user(domain_user_to_update)
    domain_user_updated = user_service.get_user(uuid)

    assert domain_user_updated.first_name == 'XXXX'
    assert domain_user_updated.last_name == 'ZZZZ'
    assert domain_user_updated.username == 'YYYY'


@pytest.mark.mongomock
def test_user_service_delete_an_user(mongodb):
    '''assert when services delete a user correctly'''
    user_service = UserService(UserUOW(mongodb))

    uuid = '221781d0-ad9a-4827-b6a4-929f61c07449'
    domain_user_from_services = user_service.get_user(uuid)
    assert len(user_service.list_all_users()) == 17

    user_service.delete_user(domain_user_from_services)
    assert len(user_service.list_all_users()) == 16


@pytest.mark.mongomock
def test_user_service_list_users(mongodb):
    '''assert when services list a users correctly'''
    user_service = UserService(UserUOW(mongodb))
    assert all(isinstance(domain_user, User) for domain_user in user_service.list_all_users())
    assert len(user_service.list_all_users()) == 17
