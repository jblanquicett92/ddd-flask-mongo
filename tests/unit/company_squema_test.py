"""This file has the purpose of test companies in json format"""
from __future__ import annotations

from src.layers.distribuited_services.bridge.serializer.json.company_schema import (
    CompanySchema,
)
from src.layers.distribuited_services.bridge.utils.formatter import is_json, json
from src.layers.domain.model.company import Company


def make_companies():
    """Fixture will generate compaies in memory"""
    return [
        Company('organization', '6625330'),
        Company('teams', '558015'),
        Company('swvl', '777666'),
        Company('rentals', '12212'),
        Company('amazonia', '10100101'),
    ]


def test_company_in_json_format():
    """assert when a company has json format"""
    company_json_schema = CompanySchema()
    testeable_company = make_companies(
    )[0]  # In Prod env, please remove this little line for a uow.company.find({})
    company_serializated = company_json_schema.dump(testeable_company)
    company_json = json.dumps(company_serializated, indent=2)

    assert is_json(company_json) is True


def test_list_of_companies_in_json_format():
    """assert when a list of companies has json format"""

    company_json_schema = CompanySchema()
    testeable_companies = make_companies()
    # In Prod env, please remove this little line for a uow.company.list() or similar
    list_of_companies = [company_json_schema.dump(company) for company in testeable_companies]
    list_of_companies_in_json_format = json.dumps(list_of_companies, indent=2)

    assert is_json(list_of_companies_in_json_format) is True
    assert len(testeable_companies) == 5
