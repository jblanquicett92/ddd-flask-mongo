'''Intention: Register subscriptions with a broker, letting the broker
 perform the filtering'''
from __future__ import annotations

import abc


class AbstractSubscriber(abc.ABC):
    """Abstract class with the purpose of register
    subscriptions with a broker, letting the broker perform the filtering"""

    @abc.abstractmethod
    def update(self):
        """Update call"""
        raise NotImplementedError
