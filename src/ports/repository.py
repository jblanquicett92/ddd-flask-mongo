'''Intention: provide CRUD methods and be injected in the uow'''
from __future__ import annotations

import abc


class AbstractRepository(abc.ABC):
    """Abstract class with the purpose of provide CRUD methods
    and be injected in the uow"""

    @abc.abstractmethod
    def add(self, model):
        """
        Adds domain model

        Args:

        model: Domain model object

        Returns:

        None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        """
        get domain model

        Args:

        reference: id, uuid or any unique identifier of the domain model object

        Returns:

        model
        """
        raise NotImplementedError

    @abc.abstractmethod
    def list_all(self):
        """
        get dictionary of domain model

        Returns:

        domain model
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, model):
        """
        update domain model

        Args:

        model: Domain model object

        Returns:

        None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, model):
        """
        delete domain model

        Args:

        model: Domain model object

        Returns:

        None
        """
        raise NotImplementedError
