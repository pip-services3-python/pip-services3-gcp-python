# -*- coding: utf-8 -*-
from .DummyCloudFunctionFixture import DummyCloudFunctionFixture


class TestDummyFunctionService:
    fixture: DummyCloudFunctionFixture

    def setup_method(self):
        self.fixture = DummyCloudFunctionFixture('handler', 3002)
        self.fixture.start_cloud_service_func_locally()

    def teardown_method(self):
        self.fixture.stop_cloud_service_locally()

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
