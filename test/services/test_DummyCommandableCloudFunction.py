# -*- coding: utf-8 -*-
from .DummyCloudFunctionFixture import DummyCloudFunctionFixture


class TestDummyCommandableCloudFunctionService:
    fixture: DummyCloudFunctionFixture

    def setup_method(self):
        self.fixture = DummyCloudFunctionFixture('commandable_handler', 3001)
        self.fixture.start_cloud_service_func_locally()

    def teardown_method(self):
        self.fixture.stop_cloud_service_locally()

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
