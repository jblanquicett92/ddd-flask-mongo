from __future__ import annotations

import json

from src.layers.distribuited_services.application import app
from src.layers.distribuited_services.bridge.controller.company_request_handler import (
    CompanyRequestHandler,
)
from src.layers.distribuited_services.endpoints.v4 import company_view
from src.layers.persistence.uow.company_uow import CompanyUOW
from src.layers.services.company_service import CompanyService


def init_services(mongodb):
    company_view.company_services = CompanyService(CompanyUOW(mongodb))
    company_view.company_request_handler = CompanyRequestHandler(company_view.company_services)


def test_company_view_create_a_company_happy_path(mongodb):

    init_services(mongodb)

    payload = {
        'name': 'New_Company',
        'phone': '+5255112033',
        'email': 'info@new_company.com',
    }
    response = app.test_client().post(
        '/v4/company/',
        data=json.dumps(payload),
        content_type='application/json',
    )

    company_created = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 201
    assert company_created['email'] == 'info@new_company.com'
    assert company_created['name'] == 'New_Company'
    assert company_created['phone'] == '+5255112033'
    assert company_created['is_active'] is True


def test_company_view_list_all_companies_happy_path(mongodb):

    init_services(mongodb)

    response = app.test_client().get('/v4/companies/?page=1&showing_range=5')

    resources = json.loads(response.data.decode('utf-8')).get('resource')
    pages = json.loads(response.data.decode('utf-8')).get('pages')

    assert response.status_code == 200

    assert resources[0]['name'] == 'organization'
    assert resources[1]['name'] == 'organization2.0'
    assert pages == 2


def test_list_all_companies_sort_by_name_asc(mongodb):

    init_services(mongodb)
    response = app.test_client().get('/v4/companies/sort_by_name/asc?page=1&showing_range=30')

    resources = json.loads(response.data.decode('utf-8')).get('resource')

    assert response.status_code == 200
    assert resources[0]['name'] == 'amazon'
    assert resources[1]['name'] == 'izzi'
    assert resources[2]['name'] == 'mercado libre'


def test_list_all_companies_sort_by_name_desc(mongodb):

    init_services(mongodb)
    response = app.test_client().get('/v4/companies/sort_by_name/desc?page=1&showing_range=30')

    resources = json.loads(response.data.decode('utf-8')).get('resource')

    assert response.status_code == 200
    assert resources[0]['name'] == 'organization3.0'
    assert resources[1]['name'] == 'organization2.0'
    assert resources[2]['name'] == 'organization'


def test_filter_companies_by_name_ama(mongodb):

    init_services(mongodb)
    response = app.test_client().get('/v4/companies/filter_by_name/ama?page=1&showing_range=30')

    resources = json.loads(response.data.decode('utf-8')).get('resource')

    assert response.status_code == 200
    assert resources[0]['name'] == 'amazon'


def test_filter_companies_by_name_me(mongodb):

    init_services(mongodb)
    response = app.test_client().get('/v4/companies/filter_by_name/me?page=1&showing_range=30')

    resources = json.loads(response.data.decode('utf-8')).get('resource')

    assert response.status_code == 200
    assert resources[0]['name'] == 'mercado libre'


def test_filter_companies_by_name_i(mongodb):

    init_services(mongodb)
    response = app.test_client().get('/v4/companies/filter_by_name/i?page=1&showing_range=30')

    resources = json.loads(response.data.decode('utf-8')).get('resource')

    assert response.status_code == 200
    assert resources[0]['name'] == 'izzi'


def test_get_a_company(mongodb):

    init_services(mongodb)
    response = app.test_client().get('/v4/company/aca2df2c-ee91-48b8-832d-06ecad511c45')

    company = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert company['email'] == 'info@amazon.com'
    assert company['name'] == 'amazon'
    assert company['phone'] == '551023'
    assert company['is_active'] is True


def test_update_a_company(mongodb):

    init_services(mongodb)

    payload = {
        'name': 'Editable Company',
        'phone': '+5266666666',
        'email': 'info@editablecompany.com',
    }

    response = app.test_client().patch(
        '/v4/company/aca2df2c-ee91-48b8-832d-06ecad511c45',
        data=json.dumps(payload),
        content_type='application/json',
    )

    company = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert company['email'] == 'info@editablecompany.com'
    assert company['name'] == 'Editable Company'
    assert company['phone'] == '+5266666666'


def test_active_deactive_a_company(mongodb):

    init_services(mongodb)

    payload = {
        'is_active': 0,
    }

    response = app.test_client().patch(
        '/v4/company/aca2df2c-ee91-48b8-832d-06ecad511c45/active_deactive/',
        data=json.dumps(payload),
        content_type='application/json',
    )

    company = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert company['email'] == 'info@amazon.com'
    assert company['name'] == 'amazon'
    assert company['phone'] == '551023'
    assert company['is_active'] is False


def test_delete_a_company(mongodb):

    init_services(mongodb)
    response = app.test_client().delete('/v4/company/aca2df2c-ee91-48b8-832d-06ecad511c45')

    company = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert company['email'] == 'info@amazon.com'
    assert company['name'] == 'amazon'
    assert company['phone'] == '551023'
    assert company['is_active'] is True


def test_number_of_companies(mongodb):

    init_services(mongodb)
    response = app.test_client().get('/v4/companies/size')

    number_of_companies = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert number_of_companies['size'] == 6
