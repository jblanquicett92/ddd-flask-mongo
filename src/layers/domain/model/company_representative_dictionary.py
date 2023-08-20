'''Custom data structure that allow company representatives'''
from __future__ import annotations

from dataclasses import dataclass

from src.layers.domain.exceptions import IsNotModelError
from src.layers.domain.model.company_representative import CompanyRepresentative
from src.layers.domain.utils.base_dictionary import BaseDictionary


@dataclass
class CompanyRepresentativeDictionary(BaseDictionary):
    """UserDictionary its a custom data structure that allow users"""

    def __setitem__(self, key, item: CompanyRepresentative):
        if not isinstance(item, CompanyRepresentative):
            raise IsNotModelError('Value it is not Company Representative model')
        self.__dict__[key] = item
