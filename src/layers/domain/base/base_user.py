'''This file intention is to provide the other user type classes with a
base and avoid code duplication'''
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from uuid import uuid4

import phonenumbers
from email_validator import EmailNotValidError
from email_validator import validate_email

from src.layers.domain.exceptions import EmailFormatError
from src.layers.domain.exceptions import EmailHaveUppercaseError
from src.layers.domain.exceptions import InvalidNameError
from src.layers.domain.exceptions import NameTooLongError
from src.layers.domain.exceptions import PhoneFormatError
from src.layers.domain.utils.encrypt_cryptography import encode


@dataclass
class BaseUser:
    """Template base class for users"""

    uuid: str = field(init=False)
    username: str = field(init=False)
    first_name: str
    last_name: str
    phone: int | str | None
    phone_country_code: int | None = field(init=False)
    _email: str
    password: str
    created: datetime = field(init=False)
    modified: datetime = field(init=False)
    is_active: bool = field(init=False)

    def __post_init__(self):
        """This magic method give the capability to post processing the class after been initialized
        the reason why post processing is that the magic method of __new__ you cannot access the
        custom validation and initialization functions"""

        self.__validate()
        self.__initialize()

    def __validate(self):
        """The intent of this function is to validate that the domain model data is in its
        bounded context"""

        self._is_first_name_valid()
        self._is_last_name_valid()
        self._is_first_name_too_long()
        self._is_last_name_too_long()
        self._is_phone_number_is_valid()

    def __initialize(self):
        """The intent of this function is to initialize the domain model data according to the
        bounded context"""

        self.uuid = self.__generate_uuid()
        self.created = self.__created_at()
        self.modified = self.__modified_at()
        self.password = self.__encrypt_password(self.password)
        self.username = self.__generate_username()
        self.phone_country_code = self.__procceded_phone_country_code()
        self.phone = self.__procceded_phone_number()
        self.is_active = True

    def __created_at(self):
        return datetime.now()

    def __modified_at(self):
        return datetime.now()

    def __generate_uuid(self):
        return str(uuid4())

    @property
    def email(self):
        """Return the email"""
        return self._email

    @email.setter
    def email(self, new_email):
        """Validate the email properties like domain or unusual characters and set it"""
        new_email = new_email.lower()
        self._is_email_address_is_lower(new_email)
        self._is_email_address_is_valid(new_email)
        self._email = new_email

    def set_phone_and_code_country(self, new_phone):
        """This function sets the phone and country_code"""
        self.phone = new_phone
        self._is_phone_number_is_valid()
        self.phone_country_code = self.__procceded_phone_country_code()
        self.phone = self.__procceded_phone_number()

    def _is_first_name_valid(self):
        firstname_has_unusual_characters = any(
            char.isdigit() for char in self.first_name
        )
        if firstname_has_unusual_characters:
            raise InvalidNameError('Firstname has unusual characters')

    def _is_last_name_valid(self):
        lastname_has_unusual_characters = any(char.isdigit() for char in self.last_name)
        if lastname_has_unusual_characters:
            raise InvalidNameError('Lastname has unusual characters')

    def _is_first_name_too_long(self):
        firstname_length = len(self.first_name) > 25
        if firstname_length:
            raise NameTooLongError('Firstname is too long')

    def _is_last_name_too_long(self):
        lastname_length = len(self.first_name) > 25
        if lastname_length:
            raise NameTooLongError('Lastname is too long')

    def __encrypt_password(self, password):
        password_encrypted = encode(password).decode('utf-8')
        return password_encrypted

    def _is_phone_number_is_valid(self):
        is_valid_number = None
        try:
            phone_number = phonenumbers.parse(str(self.phone))
            is_valid_number = phonenumbers.is_valid_number(phone_number)
        except phonenumbers.NumberParseException as parse_error:
            if not is_valid_number:
                raise PhoneFormatError(f'Invalid phone number, {parse_error}') from parse_error

    def _is_email_address_is_valid(self, new_email):
        try:
            valid = validate_email(new_email)
            valid.ascii_email
        except EmailNotValidError as email_error:
            raise EmailFormatError(f'Invalid email address, {email_error}') from email_error

    def _is_email_address_is_lower(self, email):
        if not email.islower():
            raise EmailHaveUppercaseError('Email have uppercase')

    def __procceded_phone_country_code(self):
        phone_number = phonenumbers.parse(str(self.phone))
        return phone_number.country_code

    def __procceded_phone_number(self):
        phone_number = phonenumbers.parse(str(self.phone))
        return phone_number.national_number

    def __generate_username(self):
        return f'{self.first_name[0]}{self.last_name}{self.uuid[0:8]}'

    def __str__(self):
        return f'id: {self.uuid} firstname: {self.first_name} lastname: {self.last_name}'
