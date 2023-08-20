from __future__ import annotations

from src.layers.domain.exceptions import IsNotModelError
from src.layers.domain.model.company_representative import CompanyRepresentative
from src.layers.domain.model.company_representative_dictionary import (
    CompanyRepresentativeDictionary,
)


def make_company_representatives():
    return [
        CompanyRepresentative(
            'jorge', 'blanquicett', '+525580158040',
            'j.blanquicett@organization.com', 'helloworld', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),

        CompanyRepresentative(
            'armando', 'matos', '+525580158041',
            'a.matos@organization.com', 'helloworld2.0', 'ddc65e81-3439-4edd-a6d8-27808187b0fa',
        ),
    ]


def test_company_representative_create_success():
    """Assert when company representative is created successfully"""
    testeable_company_representative = make_company_representatives()[0]

    assert testeable_company_representative.first_name == 'jorge'
    assert testeable_company_representative.last_name == 'blanquicett'
    assert testeable_company_representative.phone == 5580158040
    assert isinstance(testeable_company_representative, CompanyRepresentative)


def test_company_representative_dictionary_can_add_company_representative():
    """Assert when company_representative_dictionary
    can add company_representative"""
    testeable_company_representative = make_company_representatives()[0]
    othertesteable_company_representative = make_company_representatives()[1]
    company_representative_dictionary = CompanyRepresentativeDictionary()
    company_representative_dictionary.__setitem__(
        testeable_company_representative.uuid, testeable_company_representative,
    )
    company_representative_dictionary.__setitem__(
        othertesteable_company_representative.uuid, othertesteable_company_representative,
    )

    assert len(company_representative_dictionary) == 2


def test_company_representative_dictionary_can_only_add_company_representative():
    """Assert if exception is raised when company_representative_dictionary try"""
    """to add an object that is not of type CompanyRepresentative"""
    errored_company_representative = object()
    company_representative_dictionary = CompanyRepresentativeDictionary()
    try:
        company_representative_dictionary.__setitem__(
            1, errored_company_representative,
        )
        assert False
    except IsNotModelError as e:
        assert e.args[0] == 'Value it is not Company Representative model'


def test_company_representative_update_success():
    """Assert when company_representative is update successfully"""
    testeable_company_representative = make_company_representatives()[0]
    testeable_company_representative.first_name = 'super'
    testeable_company_representative.last_name = 'root'
    testeable_company_representative.phone = '558015'

    assert testeable_company_representative.first_name == 'super'
    assert testeable_company_representative.last_name == 'root'
    assert testeable_company_representative.phone == '558015'


def test_company_representative_deactivate_success():
    """Assert when company_representative is deactivate successfully"""
    testeable_company_representative = make_company_representatives()[0]
    testeable_company_representative.is_active = False

    assert testeable_company_representative.is_active is False
