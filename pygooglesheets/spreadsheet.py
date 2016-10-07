from apiclient import discovery
import types

class Spreadsheet:

    def __init__(self, id):
        self.id = id


    def update(self, connection, range, data):
        service_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = discovery.build('sheets', 'v4', http=connection,
                          discoveryServiceUrl=service_url)

        def map_to_json_supported_types(row):
            return [x if isinstance(x,(int, float)) else str(x) for x in row]

        body = {
            'values': [map_to_json_supported_types(row) for row in data]
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=self.id, range=range,
            valueInputOption="RAW", body=body).execute()

        return result
