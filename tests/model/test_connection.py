import pytest

import pygooglesheets
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


@pytest.fixture(scope='function')
def mock_google_service_account(request, mocker):
    mocker.patch.object(ServiceAccountCredentials, 'from_json_keyfile_name')

    test_service_account_credentials = mocker.patch(
        'oauth2client.service_account.ServiceAccountCredentials')
    test_service_account_credentials.authorize.return_value = httplib2.Http()
    ServiceAccountCredentials.from_json_keyfile_name.return_value = test_service_account_credentials
    return ServiceAccountCredentials


@pytest.fixture(scope='function')
def credentials_file(request):
    return 'tests/fixtures/service-account.json'


class TestConnection:

    class TestCreatingConnections:

        def test_passes_credentials_to_ServiceAccountCredentials_from_json_keyfile_name(
                self,
                mocker,
                mock_google_service_account,
                credentials_file):
            connection = pygooglesheets.Connection(credentials=credentials_file,
                                                   permissions="readonly")
            pos_args, keyword_args = mock_google_service_account.from_json_keyfile_name.call_args
            assert(pos_args == (credentials_file,))
            assert(keyword_args == {'scopes':'https://www.googleapis.com/auth/spreadsheets.readonly'})

        def test_it_returns_an_http_object(self,
                                           mocker,
                                           mock_google_service_account,
                                           credentials_file):
            connection = pygooglesheets.Connection(credentials=credentials_file,
                                                   permissions="readonly")
            assert(isinstance(connection, httplib2.Http))
