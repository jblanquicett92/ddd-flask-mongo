'''This file intention is to provide repository for account manager'''
from __future__ import annotations

from src.ports.repository import AbstractRepository


class AccountManagerRepository(AbstractRepository):
    '''is an implementation of the abstract class of repository with cruds methods'''

    def __init__(self, session):
        self.session = session
        self.collection = self.session.account_manager

    def add(self, model):
        self.collection.insert_one(model.__dict__)

    def get(self, reference):
        return self.collection.find_one(reference)

    def list_all(self):
        return list(self.collection.find())

    def update(self, model):
        self.collection.update_one({'_id': model._id}, {'$set': model.__dict__})

    def delete(self, model):
        self.collection.delete_one({'_id': model._id})
