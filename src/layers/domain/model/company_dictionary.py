'''Custom data structure that allow companies'''
from __future__ import annotations

from src.layers.domain.exceptions import IsNotModelError
from src.layers.domain.model.company import Company
from src.layers.domain.utils.base_dictionary import BaseDictionary


class CompanyDictionary(BaseDictionary):
    """CompanyDictionary its a custom data structure that allow companies"""

    def __setitem__(self, key, item: Company):
        if not isinstance(item, Company):
            raise IsNotModelError('Value it is not Company model')
        self.__dict__[key] = item
