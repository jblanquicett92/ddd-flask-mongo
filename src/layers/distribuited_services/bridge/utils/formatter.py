"""This file has the purpose of"""
from __future__ import annotations

import json


def is_json(object_in_json_format):
    """..."""
    try:
        json.loads(object_in_json_format)
    except ValueError:
        return False
    return True
