from __future__ import annotations

from pymongo import MongoClient

from src.ports.persistence import Config
from src.ports.persistence import DataBaseConnect


class mongo_dabatase_config(Config):
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port


class mongo_dabatase_session(DataBaseConnect):
    def __init__(self, connection_pool):
        self.session = None
        self.connection_pool = connection_pool

    def connect(self):
        client = MongoClient(
            self.connection_pool, connect=False,
        )
        self.session = client['companies']

    def get_session(self):
        return self.session
