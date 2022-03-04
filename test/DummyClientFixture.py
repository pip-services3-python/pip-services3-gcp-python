# -*- coding: utf-8 -*-
from pip_services3_commons.data import PagingParams, FilterParams

from .Dummy import Dummy
from .IDummyClient import IDummyClient


class DummyClientFixture:

    def __init__(self, client: IDummyClient):
        self.__client = client

    def test_crud_operations(self):
        dummy1 = Dummy(id=None, key="Key 1", content="Content 1")
        dummy2 = Dummy(id=None, key="Key 2", content="Content 2")

        # Create one dummy
        created_dummy1 = self.__client.create_dummy(None, dummy1)
        assert created_dummy1 is not None
        assert created_dummy1.content, dummy1.content
        assert created_dummy1.key, dummy1.key
        dummy1 = created_dummy1

        # Create another dummy
        created_dummy2 = self.__client.create_dummy(None, dummy2)
        assert created_dummy2 is not None
        assert created_dummy2.content, dummy2.content
        assert created_dummy2.key, dummy2.key
        dummy2 = created_dummy2

        # Get all dummies
        dummy_data_page = self.__client.get_dummies(
            None,
            FilterParams(),
            PagingParams(0, 5, False)
        )

        assert dummy_data_page is not None
        assert len(dummy_data_page.data) >= 2

        # Update the dummy
        dummy1.content = 'Updated Content 1'
        updated_dummy1 = self.__client.update_dummy(None, dummy1)
        assert updated_dummy1 is not None
        assert updated_dummy1.content == dummy1.content
        assert updated_dummy1.key == dummy1.key
        dummy1 = updated_dummy1

        # Delete dummy
        self.__client.delete_dummy(None, dummy1.id)

        dummy = self.__client.get_dummy_by_id(None, dummy1.id)
        assert dummy or None is None
