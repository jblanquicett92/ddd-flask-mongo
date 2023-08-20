'''Intention: post messages to an intermediary message
 broker or event bus'''
from __future__ import annotations

import abc


class AbstractPublisher(abc.ABC):
    """Abstract class with the purpose of post messages to an intermediary
    message broker or event bus"""

    @abc.abstractmethod
    def attach(self, observer):
        """Attach a observer"""
        raise NotImplementedError

    @abc.abstractmethod
    def detach(self, observer):
        """Detach a observer"""
        raise NotImplementedError

    @abc.abstractmethod
    def notify(self):
        """Notifies observers that are registered to that subject of
        any state changes that occur."""
        raise NotImplementedError
