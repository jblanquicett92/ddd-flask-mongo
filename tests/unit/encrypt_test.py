from __future__ import annotations

from src.layers.domain.utils.encrypt_cryptography import decode
from src.layers.domain.utils.encrypt_cryptography import encode


def test_correct_encode():
    """Assert when encode method successfully encrypt a string"""
    enconding = encode('j.blanquicett@')
    assert enconding != 'j.blanquicett@'


def test_correct_encode_and_decode():
    """Assert when encode and decode method It works well"""
    enconding = encode('j.blanquicett@')
    decoding = decode(enconding)
    assert decoding == 'j.blanquicett@'


def test_correct_decode():
    """Assert when decode method successfully decrypt a string"""
    secret_encode = bytes(
        r'''\gAAAAABiVdPtUZMTpZBDxbixfJhfSa-rhReXZa4-aRmsF0jv3K7EhsO4BmNgA6MbxHQ80VszQW
        wz2LhuDBJX1SBv3GjRf4qrpCf8BvZSlMZKsftPubup2eg=''', 'UTF-8',
    )
    secret_decode = decode(secret_encode)
    assert secret_decode == 'this_is_for_testing_purposses'
