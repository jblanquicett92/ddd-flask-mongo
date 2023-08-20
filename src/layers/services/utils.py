import re


# ID_REGEX = r'/[-\w]{25,}/'
# ID_REGEX = r'/[-\w]{25,}(?!.*[-\w]{25,})/'
ID_REGEX = r'/.*[^-\w]([-\w]{25,})[^-\w]?.*/'


def get_spreadsheet_id_from_url(url: str):
    search_spreadsheet = re.split(ID_REGEX, url)
    
    return search_spreadsheet[1]
