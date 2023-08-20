'''This file intention is to provide uow for user'''
from __future__ import annotations

from src.adapters.persistence.bootstrap import start_engine
from src.layers.persistence.repository.user_repository import UserRepository
from src.ports.uow import AbstractUnitOfWork


class UserUOW(AbstractUnitOfWork):
    '''is an implementation of the abstract class of unit of work
    with implementation of magic methods'''

    def __init__(self, session_factory=start_engine()):
        self.session_factory = session_factory
        self.user = UserRepository(self.session_factory)

    def __enter__(self):
        # pylint: disable=attribute-defined-outside-init
        self.session = self.session_factory
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
