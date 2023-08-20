from __future__ import annotations

from src.layers.domain.exceptions import IsNotModelError
from src.layers.domain.model.company import Company
from src.layers.domain.model.company_dictionary import CompanyDictionary
from src.layers.domain.model.company_representative import CompanyRepresentative


def make_companies():
    return [
        Company('organization', '6625330'),
        Company('teams', '558015'),
    ]


def make_company_representatives():
    return [
        CompanyRepresentative(
            'jorge', 'blanquicett', '+525580158040', 'j.blanquicett@organization.com',
            'helloworld', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),

        CompanyRepresentative(
            'armando', 'matos', '+525580158040', 'a.matos@organization.com',
            'helloworld2.0', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    ]


def connection_pool_to_google_spreadsheets(sheet_id: str, sheet_name: str):
    return f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


def test_company_create_success():
    """Assert when company is created successfully"""

    testeable_company = make_companies()[0]
    assert testeable_company.name == 'organization'
    assert testeable_company.phone == '6625330'
    assert isinstance(testeable_company, Company)


def test_company_dictionary_can_add_company():
    """Assert when company_dictionary can add companies"""

    testeable_company = make_companies()[0]
    othertesteable_company = make_companies()[1]
    companies_dictionary = CompanyDictionary()
    companies_dictionary.__setitem__(testeable_company.uuid, testeable_company)
    companies_dictionary.__setitem__(
        othertesteable_company.uuid, othertesteable_company,
    )

    assert len(companies_dictionary) == 2


def test_company_dictionary_can_only_add_company():
    """Assert if exception is raised when company dictionary try"""
    """to add an object that is not of type Company"""

    errored_company = object()
    companies_dictionary = CompanyDictionary()
    try:
        companies_dictionary.__setitem__(1, errored_company)
        assert False
    except IsNotModelError as e:
        assert e.args[0] == 'Value it is not Company model'


def test_company_can_add_company_representative():

    testeable_company = make_companies()[0]

    testeable_company_representative = make_company_representatives()[0]
    othertesteable_company_representative = make_company_representatives()[1]

    testeable_company.add_company_representative(
        testeable_company_representative,
    )
    testeable_company.add_company_representative(
        othertesteable_company_representative,
    )

    assert len(testeable_company.company_representatives) == 2
