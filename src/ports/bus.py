'''Intention: Connect to a message broker and
Manage and handle legacy and microservices changes'''
from __future__ import annotations

import abc


class AbstractBusMessage(abc.ABC):
    """Abstract class with the purpose of manage
    and handle legacy and ms changes"""

    @abc.abstractmethod
    def main(self):
        """setup and manage setup bus message"""
        raise NotImplementedError

    @abc.abstractmethod
    def handle_legacy_change(self):
        """Intention: suscribe to a broker and topic and handle
        legacy change"""
        raise NotImplementedError

    @abc.abstractmethod
    def handle_ms_change(self):
        """Intention: suscribe to a topic and broker and handle
        microservices change"""
        raise NotImplementedError
