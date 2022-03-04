# -*- coding: utf-8 -*-
import os
import subprocess
import time

import requests
from pip_services3_commons.data import FilterParams, PagingParams
from requests.packages.urllib3.util.retry import Retry

from ..Dummy import Dummy
from ..IDummyClient import IDummyClient


class DummyClientFixture:

    def __init__(self, client: IDummyClient, function_name: str, port: int = 3000):
        self._client = client
        self._port: int = port
        self._process: subprocess.Popen = None
        self._function_name: str = function_name
        self._base_url = f'http://localhost:{self._port}'

    def start_cloud_service_func_locally(self):
        self._process = subprocess.Popen(
            [
                'functions-framework',
                '--target', self._function_name,
                '--signature-type', 'http',
                # '--source', 'test/services'
                '--port', str(self._port)
            ],
            cwd=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services'),
            # stdout=subprocess.PIPE
        )

        retry_policy = Retry(total=6, backoff_factor=1)
        retry_adapter = requests.adapters.HTTPAdapter(
            max_retries=retry_policy)

        session = requests.Session()
        session.mount(self._base_url, retry_adapter)

        time.sleep(1)

    def stop_cloud_service_locally(self):
        self._process.kill()
        self._process.wait()
        self._process = None

    def test_crud_operations(self):
        DUMMY1 = Dummy(None, 'Key 1', 'Content 1')
        DUMMY2 = Dummy(None, 'Key 2', 'Content 2')

        # Create one dummy
        dummy1 = self._client.create_dummy(None, DUMMY1)

        assert dummy1 is not None
        assert dummy1.content, DUMMY1.content
        assert dummy1.key, DUMMY1.key

        # Create another dummy
        dummy2 = self._client.create_dummy(None, DUMMY2)

        assert dummy2 is not None
        assert dummy2.content, DUMMY2.content
        assert dummy2.key, DUMMY2.key

        # Get all dummies
        page = self._client.get_dummies(
            None,
            FilterParams(),
            PagingParams(0, 5, False)
        )

        assert len(page.data) >= 2

        # Update the dummy
        dummy1.content = 'Updated Content 1'
        updated_dummy1 = self._client.update_dummy(None, dummy1)

        assert updated_dummy1.id == dummy1.id
        assert updated_dummy1.content == dummy1.content
        assert updated_dummy1.key == dummy1.key
        dummy1 = updated_dummy1

        # Delete dummy
        deleted = self._client.delete_dummy(None, dummy1.id)

        assert deleted.id == dummy1.id
        assert deleted.content == dummy1.content
        assert deleted.key == dummy1.key

        dummy = self._client.get_dummy_by_id(None, dummy1.id)

        assert dummy is None
