'''This file intention is to provide the custom domain exception
that limit the field of action of domain models and limit them to their bounded context
'''
from __future__ import annotations


class BaseCustomException(Exception):
    """Base custom exception"""
    ...


class IsNotModelError(BaseCustomException):
    """Raised when value it is not domain model"""
    ...

class ModelNeedAtrribute(BaseCustomException):
    """Raised when domain model need a attribute"""
    ...


class InvalidNameError(BaseCustomException):
    """Raised when Names (first, lastname) have a unusual characters like numbers"""
    ...


class NameTooLongError(BaseCustomException):
    """Raised when Names (first, lastname) lenght is more longer than expected in the model"""
    ...


class PhoneFormatError(BaseCustomException):
    """Raised when phone have a wrong format"""
    ...


class EmailFormatError(BaseCustomException):
    """Raised when email have a wrong format"""
    ...


class EmailHaveUppercaseError(BaseCustomException):
    """Raised when email have a uppercase"""
    ...


class InvalidAsignedCreditError(BaseCustomException):
    """Raised when asigned credit is less than 0"""
    ...
