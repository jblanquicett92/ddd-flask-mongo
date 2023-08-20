from __future__ import annotations

from src.layers.domain.model.company_representative import CompanyRepresentative
from src.layers.persistence.uow.company_representative_uow import CompanyRepresentativeUOW
from src.layers.persistence.utils.company_representative_serializer import (
    CompanyRepresentativeSerializer as Serializer,
)


class RepresentativeService:
    '''
    RepresentativeService class
    Define functionality on service layer
    '''

    def __init__(self, representative_uow: CompanyRepresentativeUOW):
        self.representative_uow = representative_uow

    def add_company_representative(self, representative: CompanyRepresentative):
        '''
        Add Representative data to domain model on DB
        function.

        :param representative: CompanyRepresentative entity domain model
        '''

        self.representative_uow.company_representative.add(representative)
        return representative

    def update_company_representative(self, representative_to_updated: CompanyRepresentative):
        '''
        Update Representative data to domain model on DB
        function.

        :param representative_to_updated: Company representative object with
                                       data to update
        '''

        self.representative_uow.company_representative.update(representative_to_updated)
        return representative_to_updated

    def delete_company_representative(self, representative_to_deleted: CompanyRepresentative):
        '''
        Delete Representative data to domain model on DB
        function.

        :param representative_to_deleted: Company representative dictionary with data
                                            to delete
        '''

        self.representative_uow.company_representative.delete(representative_to_deleted)
        return representative_to_deleted

    def get_company_representative(self, representative_uuid):
        '''
        Retrieve by UUID attribute User Representative data from DB
        function.

        :param representative_uuid: Company Representative UUID with data
                                    to get
        '''

        representative_dict_from_mongo_db = self.representative_uow.company_representative.get(
            {'uuid': representative_uuid},
        )

        representative_serializer = Serializer(representative_dict_from_mongo_db)
        domain_representative = representative_serializer.company_representative

        return domain_representative

    def list_all_representatives(self):
        '''
        Retrieve all Representatives data from DB function
        '''

        reprensentatives = self.representative_uow.company_representative.list_all()

        return [Serializer(reprensentative).company_representative for reprensentative in reprensentatives]

    def list_all_representatives_by_company(self, company_uuid):
        '''
        Retrieve all Representatives data from DB function
        '''

        reprensentatives = self.representative_uow.company_representative.list_all_compound_by(company_uuid)

        return [Serializer(reprensentative).company_representative for reprensentative in reprensentatives]
