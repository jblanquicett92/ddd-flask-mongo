"""This file has the purpose of test company representatives in json format"""
from __future__ import annotations

from src.layers.distribuited_services.bridge.serializer.json.company_representative_schema import (
    CompanyRepresentativeSchema,
)
from src.layers.distribuited_services.bridge.utils.formatter import is_json, json
from src.layers.domain.model.company_representative import CompanyRepresentative


def make_company_representatives():
    """Fixture will generate company representatives in memory"""
    return [
        CompanyRepresentative(
            'jorge', 'blanquicett',
            '+525580158040', 'j.blanquicett@organization.com',
            'helloworld', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
        CompanyRepresentative(
            'armando', 'matos',
            '+525580158041', 'a.matos@organization.com',
            'helloworld2.0', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    ]


def test_company_representative_in_json_format():
    """assert when a company has json format"""
    testeable_company_representative = make_company_representatives(
    )[0]  # In Prod env, please remove this little line for a uow.company_representative.find({})
    company_representative_json_schema = CompanyRepresentativeSchema()
    company_representative_serializated = company_representative_json_schema.dump(testeable_company_representative)
    company_representative_json = json.dumps(company_representative_serializated, indent=2)

    assert is_json(company_representative_json) is True


def test_list_of_company_representatives_in_json_format():
    """assert when a list of companies has json format"""

    company_representative_json_schema = CompanyRepresentativeSchema()
    # In Prod env, please remove this little line for a uow.company_representative.list() or similar
    testeable_company_representatives = make_company_representatives()
    list_of_company_representatives = [
        company_representative_json_schema.dump(
            company,
        ) for company in testeable_company_representatives
    ]
    list_of_company_representatives_in_json_format = json.dumps(list_of_company_representatives, indent=2)

    assert is_json(list_of_company_representatives_in_json_format) is True
    assert len(testeable_company_representatives) == 2
