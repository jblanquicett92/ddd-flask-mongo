'''This file intention is to provide the class user
and its business rules'''
from __future__ import annotations

from dataclasses import dataclass

from src.layers.domain.base.base_user import BaseUser
from src.layers.domain.exceptions import InvalidAsignedCreditError


@dataclass
class User(BaseUser):
    """Person benefited by the company to be transferred from home to work in an organization"""

    asigned_credits: float
    company_uuid: str

    def __post_init__(self):
        super().__post_init__()
        self.__validate()

    def __validate(self):
        self._is_asigned_credits_are_float()
        self._is_asigned_credits_valid()

    def _is_asigned_credits_valid(self):
        is_asigned_credits_valid = self.asigned_credits < 0
        if is_asigned_credits_valid:
            raise InvalidAsignedCreditError('Asigned credit cant be less than 0')

    def _is_asigned_credits_are_float(self):
        is_asigned_credits_valid = isinstance(self.asigned_credits, float)
        if not is_asigned_credits_valid:
            raise InvalidAsignedCreditError('Asigned credit is not instace of float')
