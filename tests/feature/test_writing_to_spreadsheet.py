import pytest
import pygooglesheets
from datetime import datetime, timedelta

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import httplib2


def read_from_sheet(sheet_id, range, credentials):
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range).execute()
    return result


class TestFeatureSpecsWritingToSheet:

    # To run this test you need a valid Service Account json credentials file in
    # tests/fixtures/service-account-private.json. The spreadsheet it is writing
    # to is globally accessible so no special permissions needed there.
    def test_write_to_spreadsheet(self):
        credentials = 'tests/fixtures/service-account-private.json'
        connection = pygooglesheets.Connection(credentials=credentials,
                                               permissions="readwrite")
        spreadsheet = pygooglesheets.Spreadsheet(
            '1fgOEqugOhbsV_Ntq53xqY40i3otkA-4Qq-uzQaT1q3M')
        interval_start = datetime.strptime(
            "01/01/15 00:00:00", "%d/%m/%y %H:%M:%S")

        def interval_generator(start, end, increment):
            while start < end:
                next_item = start + increment
                yield (start, next_item)
                start = next_item
        intervals = interval_generator(datetime.strptime("01/01/15 00:00:00", "%d/%m/%y %H:%M:%S"),
                                       datetime.strptime(
                                           "01/01/15 03:00:00", "%d/%m/%y %H:%M:%S"),
                                       timedelta(hours=1))
        widget_counts = [15, 18, 27]
        data = [list(interval + (widget_counts[i],))
                for i, interval in enumerate(intervals)]
        empty_data = [['', '', ''], ['', '', ''], ['', '', '']]
        range = "A1:C3"
        spreadsheet.update(connection, range, empty_data)

        result = read_from_sheet(spreadsheet.id, range, credentials)
        assert(result.get('values') is None)

        spreadsheet.update(connection, "A1:C3", data)
        result = read_from_sheet(spreadsheet.id, range, credentials)

        expected = map(lambda row: [str(x) for x in row], data)
        assert(result.get('values') == expected)
