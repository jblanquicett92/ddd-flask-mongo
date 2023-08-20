from __future__ import annotations

from pytest_mongodb import plugin

from src.adapters.persistence.bootstrap import start_engine
from src.layers.domain.model.company import Company


def test_mongo_engine(pytestconfig):
    assert plugin.mongo_engine() == 'mongomock'


def test_mongo_db_can_retrieve_collections(mongodb):
    assert 'company' in mongodb.list_collection_names()


def test_mongo_db_find_collection(mongodb):
    organization = mongodb.company.find_one({'name': 'organization'})
    assert organization['phone'] == 558015


def test_mongo_db_can_insert_data_to_a_collection(mongodb):

    testeable_company = Company('team', '111222')
    mongodb.company.insert_one(testeable_company.__dict__)
    find_testeable_company_on_db = mongodb.company.find_one({'name': 'team'})

    assert find_testeable_company_on_db['name'] == testeable_company.name


def test_mongo_db_can_count_documents(mongodb):
    assert mongodb.company.count_documents({}) == 6


def test_mongo_db_singleton_start_engine():
    '''Assert when we have 3 or more instances of mongo clients but
    this instances have the same memory address'''
    mongodb_client1 = start_engine()
    mongodb_client2 = start_engine()
    mongodb_client3 = start_engine()

    assert hex(id(mongodb_client1)) == hex(id(mongodb_client2))
    assert hex(id(mongodb_client1)) == hex(id(mongodb_client3))
    assert hex(id(mongodb_client2)) == hex(id(mongodb_client3))
