from __future__ import print_function
import pytest
import pygooglesheets
from datetime import datetime, timedelta

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import httplib2


def list_sheets(credentials):
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    result = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'").execute()
    return result

def delete_file(credentials, file_id):
    SCOPES = 'https://www.googleapis.com/auth/drive'
    c = ServiceAccountCredentials.from_json_keyfile_name(
        credentials, scopes=SCOPES)
    http = c.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    print("Deleting file {}".format(file_id))
    result = service.files().delete(fileId=file_id).execute()
    return result

@pytest.fixture(scope='function')
def files(request):
    credentials = request.node.get_marker('credentials').args[0]
    expected_name = request.node.get_marker('expected_name').args[0]
    original_files = list_sheets(credentials).get('files')

    original_ids = [ f['id'] for f in original_files ]
    yield original_files

    new_files = list_sheets(credentials).get('files')
    # This is a little sketchy because there may be race conditions... not sure
    # how else to handle
    files_to_remove = [ f for f in new_files if f['name'] == expected_name ] #and f['id'] not in original_ids ]
    for f in files_to_remove:
        delete_file(credentials, f['id'])



class TestFeatureSpecs:

    # To run this test you need a valid Service Account json credentials file in
    # tests/fixtures/service-account-private.json. The spreadsheet it is writing
    # to is globally accessible so no special permissions needed there.
    @pytest.mark.credentials('tests/fixtures/service-account-private.json')
    @pytest.mark.expected_name('Test Sheet')
    def test_create_spreadsheet(self, request, files):
        credentials = request.node.get_marker('credentials').args[0]
        connection = pygooglesheets.Connection(credentials=credentials,
                                               permissions="readwrite")

        expected_name = request.node.get_marker('expected_name').args[0]

        starting_files = files
        count_files_matching_expected_name = len([f for f in starting_files if f['name'] == expected_name])
        assert(count_files_matching_expected_name == 0 )

        spreadsheet = pygooglesheets.Spreadsheet.create(connection=connection, name=expected_name)
        result = list_sheets(credentials)
        count_files_matching_expected_name = len([f for f in result.get('files') if f['name'] == expected_name])
        assert(count_files_matching_expected_name == 1)

        delete_file(credentials, spreadsheet.id)
