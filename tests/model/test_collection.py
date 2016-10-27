import pytest

import pygooglesheets
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


class TestCollection:

    def test_collection_exists(self):
        assert hasattr(pygooglesheets, 'collection')

    class TestCreate:

        def test_collection_create_exists_and_can_be_called(self):
            assert hasattr(pygooglesheets.collection, 'create') and callable(pygooglesheets.collection.create)

        def test_collection_create_raises_exception_when_called_with_nothing(self):
            with pytest.raises(Exception):
                pygooglesheets.collection.create()

        def test_collection_create_requires_connection_and_name_arguments(self):
            # We want a mock connection here, but even that's not enough. We're
            # seeing issues with how the collection functions are designed in that
            # the abstractions leak and we have code internally that
            # doesn't obey demeter's law. This makes mocking very difficult
            pytest.skip()

            # No specific assert needed here - any exception would cause this to
            # fail. A possible improvement here would be to make sure we don't
            # raise a specific pygooglesheets.exception.InvalidArguments exception
            # and implement associated exception code.
            pygooglesheets.collection.create(connection, name)


        def test_collection_create_returns_Spreadsheet_when_called_with_valid_params(self):
            pytest.skip()
            # We want a mock connection here, but even that's not enough. We're
            # seeing issues with how the collection functions are designed in that
            # the abstractions leak and we have code internally that
            # doesn't obey demeter's law. This makes mocking very difficult
            assert pygooglesheets.collection.create(connection, name)
