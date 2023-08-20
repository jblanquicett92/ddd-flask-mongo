from __future__ import annotations

from datetime import datetime

from src.layers.distribuited_services.bridge.serializer.json.company_representative_schema import (
    CompanyRepresentativeSchema,
)
from src.layers.distribuited_services.bridge.utils.formatter import json
from src.layers.domain.model.company_representative import CompanyRepresentative
from src.layers.services.representative_service import RepresentativeService


class RepresentativeRequestHandler:
    '''...'''

    def __init__(self, representative_service: RepresentativeService) -> None:
        self.representative_service = representative_service
        self.representative_schema = CompanyRepresentativeSchema()

    def number_of_representatives(self):
        '''...'''
        number_of_representatives = len(self.representative_service.list_all_representatives())
        number_of_representatives = json.dumps({'number_of_representatives': number_of_representatives})
        return number_of_representatives

    def list_all_representatives(self):
        '''...'''
        # list[CompanyRepresentative]
        representatives = self.representative_service.list_all_representatives()
        # list[{'..':'..', '..':'..'}]
        representatives = [self.representative_schema.dump(representative) for representative in representatives]
        # '[{'..':'..', '..':'..'}]'
        representatives = json.dumps(representatives)
        return representatives

    def add_a_representative(self, payload):
        '''...'''
        first_name, last_name = payload['first_name'], payload['last_name']
        phone, email = payload['phone'], payload['email']
        password, company_uuid = payload['password'], payload['company_uuid']
        new_representative = CompanyRepresentative(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            _email=email,
            password=password,
            company_uuid=company_uuid,
        )

        self.representative_service.add_company_representative(new_representative)
        representative_serializated = self.representative_schema.dump(new_representative)
        representative_serializated = json.dumps(representative_serializated)
        return representative_serializated

    def get_a_representative(self, payload):
        '''...'''
        representative_uuid = payload['uuid']
        representative = self.representative_service.get_company_representative(representative_uuid)
        representative = self.representative_schema.dump(representative)
        representative = json.dumps(representative)
        return representative

    def _update(self, representative: CompanyRepresentative):

        representative.modified = datetime.now()
        representative_updated = self.representative_service.update_company_representative(representative)
        representative_serializated = self.representative_schema.dump(representative_updated)
        representative_serializated = json.dumps(representative_serializated)
        return representative_serializated

    def update_contact_info_for_a_representative(self, payload):
        '''...'''
        uuid = payload['uuid']
        representative = self.representative_service.get_company_representative(uuid)
        first_name, last_name = payload['first_name'], payload['last_name']
        phone, email = payload['phone'], payload['email']

        representative.first_name = first_name
        representative.last_name = last_name
        representative.set_phone_and_code_country(phone)
        representative.email = email

        return self._update(representative)
