'''..'''
# mypy: ignore-errors
from __future__ import annotations

import json

from flask import Blueprint
from flask import request

from src.layers.distribuited_services.bridge.controller.company_request_handler import CompanyRequestHandler
from src.layers.persistence.uow.company_uow import CompanyUOW
from src.layers.services.company_service import CompanyService

company = Blueprint('company', __name__, url_prefix='/v4/company')
companies = Blueprint('companies', __name__, url_prefix='/v4/companies')

# Initialize services and handlers
company_services = CompanyService(CompanyUOW())
company_request_handler = CompanyRequestHandler(company_services)


@company.post('/')
def create_a_company():
    '''..'''
    payload = json.loads(request.data)
    response = company_request_handler.add_a_company(payload)
    return response


@companies.get('/')
def list_all_companies():
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.list_all_companies(page, showing_range)
    return response


@companies.get('/sort_by_name/asc')
def list_all_companies_sort_by_name_asc():
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.list_all_companies_sort_by_name_asc(page, showing_range)
    return response


@companies.get('/sort_by_name/desc')
def list_all_companies_sort_by_name_desc():
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.list_all_companies_sort_by_name_desc(page, showing_range)
    return response


@companies.get('/sort_by_created/asc')
def list_all_companies_sort_by_created_asc():
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.list_all_companies_sort_by_created_asc(page, showing_range)
    return response


@companies.get('/sort_by_created/desc')
def list_all_companies_sort_by_created_desc():
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.list_all_companies_sort_by_created_desc(page, showing_range)
    return response


@companies.get('/sort_by_modified/asc')
def list_all_companies_sort_by_modified_asc():
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.list_all_companies_sort_by_modified_asc(page, showing_range)
    return response


@companies.get('/sort_by_modified/desc')
def list_all_companies_sort_by_modified_desc():
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.list_all_companies_sort_by_modified_desc(page, showing_range)
    return response


@companies.get('/filter_by_name/<name>')
def filter_companies_by_name(name):
    '''..'''
    page = request.args.get('page')
    showing_range = request.args.get('showing_range')
    response = company_request_handler.filter_companies_by_name(name, page, showing_range)
    return response


@company.get('/<uuid>')
def get_a_company(uuid):
    '''..'''
    payload = {'uuid': uuid}
    response = company_request_handler.get_a_company(payload)
    return response


@company.patch('/<uuid>')
def update_a_company(uuid):
    '''..'''
    payload = json.loads(request.data)
    payload['uuid'] = uuid
    response = company_request_handler.update_a_company(payload)
    return response


@company.patch('/<uuid>/active_deactive/')
def active_deactive_a_company(uuid):
    '''..'''
    payload = json.loads(request.data)
    payload['uuid'] = uuid
    response = company_request_handler.active_deactive_company(payload)
    return response


@company.delete('/<uuid>')
def delete_a_company(uuid):
    '''..'''
    payload = {'uuid': uuid}
    response = company_request_handler.delete_a_company(payload)
    return response


@companies.get('/size')
def get_number_of_companies():
    '''..'''
    response = company_request_handler.number_of_companies()
    return response
