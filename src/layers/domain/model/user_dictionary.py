'''Custom data structure that allow users'''
from __future__ import annotations

from src.layers.domain.exceptions import IsNotModelError
from src.layers.domain.model.user import User
from src.layers.domain.utils.base_dictionary import BaseDictionary


class UserDictionary(BaseDictionary):
    """UserDictionary its a custom data structure that allow users"""

    def __setitem__(self, key, item: User):
        if not isinstance(item, User):
            raise IsNotModelError('Value it is not User model')
        self.__dict__[key] = item
