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


@pytest.fixture(scope='function')
def sheet(request)
    # get_marker returns a tuple, but we only want the first one so...
    credentials_file = request.node.get_marker('credentials')[0]
    sheet = pygooglesheets.collections.create(
        pygooglesheets.Connection(credentials=credentials_file, permissions='readwrite'),
        name="Test Sheet for Sharing")
    yield sheet

    # For clean up we should delete the sheet
    # TODO: Make delete_sheet a test helper - we may want to make this
    #   functionality available via a SpreadsheetCollection module
    pygooglesheets.collection.delete(credentials_file, sheet.id)

class TestFeatureSpecsSharingSheet:

    # To run this test you need two valid Service Account json credentials: one
    # in tests/fixtures/service-account-private.json and another in
    # tests/fixtures/other-service-account-private.json. The other service
    # account represents the other user we are sharing with, and we'll need
    # their credentials to know that we successfully shared
    @pytest.mark.credentials('tests/fixtures/service-account-private.json')
    @pytest.mark.other_credentials('tests/fixtures/other-service-account-private.json')
    def test_share_spreadsheet(self, request, sheet):
        # Get a spreadsheet (we can just create one) - this can happen via a
        # fixture so we can use fixture finalization to delete the created sheet.

        # assert other email doesn't have access to the spreadsheet

        # Share sheet with other email

        # assert other email does have access to spreadsheet
