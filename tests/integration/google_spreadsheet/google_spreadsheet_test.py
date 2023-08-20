from __future__ import annotations

import pandas as pd
import pytest

from src.layers.services.utils import get_spreadsheet_id_from_url


def connection_pool_to_google_spreadsheets(sheet_id: str, sheet_name: str):
    return f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


def connection_pool_to_google_spreadsheets_from_id(sheet_id: str):
    return f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv'


def test_google_spreadsheet_handle_exception_if_url_is_bad():

    google_spreadsheets_url = connection_pool_to_google_spreadsheets(
        '', '',
    )
    with pytest.raises(Exception) as excinfo:
        pd.read_csv(google_spreadsheets_url, encoding='utf8')
    assert 'HTTP Error 404: Not Found' in str(excinfo.value)


def test_google_spreadsheet_if_url_is_good():

    google_spreadsheets_url = connection_pool_to_google_spreadsheets(
        '1mbyk0OfajYo2owwcmVTXuVGIIVeHj4eINZldPiSNNoU', 'template_massive_users_add',
    )

    dataframe = pd.read_csv(google_spreadsheets_url, encoding='utf8')
    assert len(dataframe) != 0


def test_google_spreadsheet_data_with_id_from_url():
    url = 'https://docs.google.com/spreadsheets/d/1mbyk0OfajYo2owwcmVTXuVGIIVeHj4eINZldPiSNNoU/gviz/tq?tqx=out:csv'
    
    # url = 'https://docs.google.com/spreadsheets/d/1w5Lkhe2wkrUTfhn1CEWEjZS5gwlndV5EKpZ25gyC_F0/edit#gid=0'
    
    spreadsheet_id = get_spreadsheet_id_from_url(url)
    
    google_spreadsheets_url = connection_pool_to_google_spreadsheets_from_id(
        spreadsheet_id
    )
    
    dataframe = pd.read_csv(google_spreadsheets_url, encoding='utf8', delimiter=",")
    
    assert len(dataframe) != 0
