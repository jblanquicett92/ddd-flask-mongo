'''TODO generate roles and permissions with this class
see the possibility of creating a new class with roles'''
from __future__ import annotations

from src.layers.domain.base.base_user import BaseUser


class AccountManager(BaseUser):
    """Person whose job is to manage companies in the teams vertical in organization"""

    # company_uuid: str
