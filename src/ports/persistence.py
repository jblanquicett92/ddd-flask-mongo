'''Intention: setup client connection pool and be
injected in DataBaseConnect'''
from __future__ import annotations

import abc


class Config(abc.ABC):
    """Abstract class with the purpose of setup client
    connection pool and be injected in DataBaseConnect"""

    @abc.abstractmethod
    def __init__(self, database, user, password, host, port):
        """This constructor have the capability setup
        connection whitouth engine"""
        raise NotImplementedError


class DataBaseConnect(abc.ABC):
    """Abstract class with the purpose of Connect to a db client"""

    @abc.abstractmethod
    def __init__(self, config: Config):
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self):
        """initialize connection or session to db client"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_session(self):
        """get the current session from the db client"""
        raise NotImplementedError
