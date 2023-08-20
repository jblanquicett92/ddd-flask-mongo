from __future__ import annotations

from src.layers.domain.exceptions import (
    EmailFormatError,
    InvalidAsignedCreditError,
    InvalidNameError,
    IsNotModelError,
    NameTooLongError,
    PhoneFormatError,
)
from src.layers.domain.model.user import User
from src.layers.domain.model.user_dictionary import UserDictionary


def make_users():
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


def test_user_create_success():
    """Assert when user is created successfully"""
    testeable_user = make_users()[0]

    assert testeable_user.first_name == 'jorge'
    assert testeable_user.last_name == 'blanquicett'
    assert testeable_user.phone == 5580158040
    assert isinstance(testeable_user, User)


def test_user_dictionary_can_add_users():
    """Assert when user_dictionary can add users"""
    testeable_user = make_users()[0]
    othertesteable_user = make_users()[1]
    user_dictionary = UserDictionary()
    user_dictionary.__setitem__(testeable_user.uuid, testeable_user)
    user_dictionary.__setitem__(othertesteable_user.uuid, othertesteable_user)

    assert len(user_dictionary) == 2


def test_user_dictionary_can_only_add_users():
    """Assert if exception is raised when user_dictionary try"""
    """to add an object that is not of type User"""
    errored_user = object()
    user_dictionary = UserDictionary()
    try:
        user_dictionary.__setitem__(1, errored_user)
    except IsNotModelError as e:
        assert e.args[0] == 'Value it is not User model'


def test_user_update_success():
    """Assert when user is update successfully"""
    testeable_user = make_users()[0]
    testeable_user.first_name = 'super'
    testeable_user.last_name = 'root'
    testeable_user.phone = '+525580158040'

    assert testeable_user.first_name == 'super'
    assert testeable_user.last_name == 'root'
    assert testeable_user.phone == '+525580158040'


def test_user_deactivate_success():
    """Assert when user is deactivate successfully"""
    testeable_user = make_users()[0]
    testeable_user.is_active = False

    assert testeable_user.is_active is False


def test_user_first_name_is_too_long():
    """Assert when custom exception interrupt system when user firstname is too long"""
    try:
        User(
            'nisistenatuserrorsitvoluptatem', 'matos',
            '6625331', 'a.matos@organization.com',
            'helloworld2.0', 50.1, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        )
    except NameTooLongError as e:
        assert e.args[0] == 'Firstname is too long'


def test_user_last_name_is_too_long():
    """Assert when custom exception interrupt system when user lastname is too long"""
    try:
        User(
            'armando', 'nisistenatuserrorsitvoluptatem',
            '+525580158040', 'a.matos@organization.com',
            'helloworld2.0', 50.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        )
    except NameTooLongError as e:
        assert e.args[0] == 'Lastname is too long'


def test_user_first_name_is_valid():
    """Assert when custom exception interrupt system when user firstname have a unusual characters like numbers"""
    try:
        User(
            'armand0', 'matos',
            '+525580158040', 'a.matos@organization.com',
            'helloworld2.0', 50.1, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    except InvalidNameError as e:
        assert e.args[0] == 'Firstname has unusual characters'


def test_user_last_name_is_valid():
    """Assert when custom exception interrupt system when user lastname have a unusual characters like numbers"""
    try:
        User(
            'armando', 'mat3os',
            '+525580158040', 'a.matos@organization.com',
            'helloworld2.0', 50, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        )
    except InvalidNameError as e:
        assert e.args[0] == 'Lastname has unusual characters'


def test_user_phone_number_have_not_region():
    """Assert when custom exception interrupt system when user phone have not region"""
    try:
        User(
            'armando', 'matos',
            '25580158040', 'a.matos@organization.com',
            'helloworld2.0', 50.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        )
    except PhoneFormatError as e:
        assert e.args[0] == 'Invalid phone number, (0) Missing or invalid default region.'


def test_user_phone_number_too_short():
    """Assert when custom exception interrupt system when user phone is to short"""
    try:
        User(
            'armando', 'matos',
            '+525', 'a.matos@organization.com',
            'helloworld2.0', 50.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        )
    except PhoneFormatError as e:
        assert e.args[0] == 'Invalid phone number, (3) The string supplied is too short to be a phone number.'


def test_user_email_good_domain_bad_period():
    """Assert when custom exception interrupt system when user email domain have not period"""
    # Bad: google facebook organization
    # OK: google.com facebook.com organization.com
    testeable_user = make_users()[0]
    try:
        testeable_user.email = 'j.blanquicett@organization'
    except EmailFormatError as e:
        assert e.args[0] == 'Invalid email address, The domain name organization is not valid. It should have a period.'


def test_user_email_bad_domain_good_period():
    """Assert when custom exception interrupt system when user email domain contain invalid characters"""
    testeable_user = make_users()[0]
    try:
        testeable_user.email = 'j.blanquicett@u r b v a n.com'
    except EmailFormatError as e:
        assert e.args[
            0
        ] == '''Invalid email address, The domain name u r b v a n.com contains '''\
            '''invalid characters (Codepoint U+0020 at position 2 of 'u r b v a n' not '''\
            '''allowed).'''


def test_user_email_good_domain_good_period():
    """Assert when custom exception interrupt system when user email domain contain invalid characters"""
    testeable_user = make_users()[0]
    testeable_user.email = 'j.blanquicett@organization.com'
    assert testeable_user.email == 'j.blanquicett@organization.com'


def test_user_asigned_credits_cant_be_negative():
    """Assert when custom exception interrupt system when user asigned credits are negative"""
    try:
        User(
            'armando', 'matos',
            '+525580158040', 'a.matos@organization.com',
            'helloworld2.0', -5.0, 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        )
    except InvalidAsignedCreditError as e:
        assert e.args[0] == 'Asigned credit cant be less than 0'


def test_user_asigned_credits_cant_be_string():
    """Assert when custom exception interrupt system when user asigned credits are not float"""
    try:
        User(
            'armando', 'matos',
            '+525580158040', 'a.matos@organization.com',
            'helloworld2.0', '7', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        )
    except InvalidAsignedCreditError as e:
        assert e.args[0] == 'Asigned credit is not instace of float'
