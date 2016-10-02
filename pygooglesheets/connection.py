import httplib2
from oauth2client.service_account import ServiceAccountCredentials

def Connection(credentials = 'service_account.json',
                permissions = 'readwrite'):
    scopes = {
        'readonly': 'https://www.googleapis.com/auth/spreadsheets.readonly',
        'r': 'https://www.googleapis.com/auth/spreadsheets.readonly',
        'readwrite': 'https://www.googleapis.com/auth/spreadsheets',
        'w': 'https://www.googleapis.com/auth/spreadsheets'
    }
    return ServiceAccountCredentials.from_json_keyfile_name(
        credentials, scopes=scopes[permissions]).authorize(httplib2.Http())
