# -*- coding: utf-8 -*-
import os

import pytest
from pip_services3_commons.config import ConfigParams

from test.clients.DummyClientFixture import DummyClientFixture
from test.clients.DummyCloudFunctionClient import DummyCloudFunctionClient

function_name = os.environ.get('GCP_FUNCTION_NAME') or 'handler'
protocol = os.environ.get('GCP_FUNCTION_PROTOCOL') or 'http'
region = os.environ.get('GCP_FUNCTION_REGION') or '3'
project_id = os.environ.get('GCP_PROJECT_ID') or '4'
uri = os.environ.get('GCP_FUNCTION_URI') or 'http://localhost:3007'

config = ConfigParams.from_tuples(
    'connection.uri', uri,
    'connection.protocol', protocol,
    'connection.region', region,
    'connection.function', function_name,
    'connection.project_id', project_id,
)


@pytest.mark.skipif(not uri and (not region or not function_name or not protocol or not project_id),
                    reason='No Azure credentials')
class TestDummyCloudFunctionClient:
    client: DummyCloudFunctionClient
    fixture: DummyClientFixture

    def setup_method(self):
        self.client = DummyCloudFunctionClient()
        self.client.configure(config)

        self.fixture = DummyClientFixture(self.client, 'handler', 3007)

        if uri == 'http://localhost:3007':
            self.fixture.start_cloud_service_func_locally()

        self.client.open(None)

    def teardown_method(self):
        self.client.close(None)

        if uri == 'http://localhost:3007':
            self.fixture.stop_cloud_service_locally()

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
