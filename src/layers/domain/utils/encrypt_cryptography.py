from __future__ import annotations

from cryptography.fernet import Fernet
from decouple import config as environment

key = Fernet.generate_key()
fernet = Fernet(bytes(environment('FERNET_SECRET_KEY'), 'UTF-8'))


def encode(string_to_encode):
    return fernet.encrypt(string_to_encode.encode())


def decode(string_to_decode):
    return fernet.decrypt(string_to_decode).decode()
