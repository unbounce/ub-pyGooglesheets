from spreadsheet import Spreadsheet
from apiclient import discovery


# create
# Create a new spreadsheet from the details passed in
def create(connection, name, sheets=[], locale='en_US'):
    service_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = discovery.build('sheets', 'v4', http=connection,
                      discoveryServiceUrl=service_url)

    body = {
        'properties': {
            'title': name,
            'locale': locale
        },
        'sheets': [ sheets ]
    }
    result = service.spreadsheets().create(body=body).execute()
    return(Spreadsheet(result['spreadsheetId']))
