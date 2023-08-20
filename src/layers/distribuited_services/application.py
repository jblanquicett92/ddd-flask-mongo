from __future__ import annotations

from flask import Flask
from flask_cors import CORS

from src.layers.distribuited_services.endpoints.v4.company_view import (
    companies,
    company,
)

app = Flask(__name__, instance_relative_config=True)

POST = 'POST'
GET = 'GET'
PATCH = 'PATCH'
DELETE = 'DELETE'

http_methods_allow = [POST, GET, PATCH, DELETE]
origins = ['organization.com']

CORS(
    app, resources={r'/v4/*'},
    origins=origins,
    methods=http_methods_allow,
    supports_credentials=True,
    vary_header=True,
)

app.register_blueprint(company)
app.register_blueprint(companies)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
