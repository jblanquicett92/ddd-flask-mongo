'''....'''
from __future__ import annotations

import json

import requests

from config import CONTENT_TYPE
from config import DEVICE
from config import OS
from config import PLATFORM
from config import TOWER_AUTH_EMAIL
from config import TOWER_AUTH_PASSWORD
from config import TOWER_BASE_URL
from config import VERSION
from src.layers.domain.model.company import Company

headers = {
    'Content-Type': CONTENT_TYPE,
    'platform': PLATFORM,
    'version': VERSION,
    'os': OS,
    'device': DEVICE,
}

base_url = TOWER_BASE_URL


def login():
    '''...'''

    payload = json.dumps({
        'email': TOWER_AUTH_EMAIL,
        'password': TOWER_AUTH_PASSWORD,
    })

    login_endpoint = f'{base_url}/v1/login/'

    response = requests.post(login_endpoint, data=payload, headers=headers)

    return response


def get_token(response):

    response = response.json()

    token = response['body']['results'][0]['session']['token']

    return token


def get_companies(token):
    '''...'''

    company_list_endpoint = f'{base_url}/v1/routes/company'
    headers['Authorization'] = f'Token {token}'
    response = requests.get(company_list_endpoint, headers=headers)

    return response


def create_company(token, company: Company):
    '''...'''

    payload = json.dumps({'name': company.name, 'ms_company_uuid':company.uuid})

    create_endpoint = f'{base_url}/v1/routes/company/'
    headers['Authorization'] = f'Token {token}'

    response = requests.post(create_endpoint, data=payload, headers=headers)

    return response
