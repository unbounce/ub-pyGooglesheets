import pytest
import inspect

import pygooglesheets
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


class TestCollection:

    def test_collection_is_module(self):
        assert(hasattr(pygooglesheets, 'collection') and inspect.ismodule(pygooglesheets.collection))

    class TestCreate:

        def test_collection_create_exists(self):
            assert(hasattr(pygooglesheets.collection, 'create') and inspect.isfunction(pygooglesheets.collection.create))
