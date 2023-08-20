'''This file intention is to provide the class company representative
and its business rules'''
from __future__ import annotations

from dataclasses import dataclass

from src.layers.domain.base.base_user import BaseUser


@dataclass
class CompanyRepresentative(BaseUser):
    """Face of the company towards organization, interested in the logistics of moving
    its employees from home to work efficiently. It is usually human resources staff"""

    company_uuid: str
