'''Intention: Manage engine db clients'''
from __future__ import annotations

import abc


class AbstractUnitOfWork(abc.ABC):
    """Abstract class with the purpose of manage engine db clients"""

    @abc.abstractmethod
    def __enter__(self):
        """Make a database connection and return it"""
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *args):
        """Make sure the dbconnection gets closed"""
        raise NotImplementedError

    @abc.abstractmethod
    def _commit(self):
        """Commits a transaction"""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        """Must be emitted in order to fully roll back the transaction."""
        raise NotImplementedError
