# -*- coding: utf-8 -*-
import os
import subprocess

import time

import requests
from pip_services3_commons.data import FilterParams, PagingParams
from requests.packages.urllib3.util.retry import Retry

from ..Dummy import Dummy


class DummyCloudFunctionFixture:

    def __init__(self, function_name: str, port: int = 3000):
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
            cwd=os.path.dirname(__file__),
            # stdout=subprocess.STDOUT
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
        res = requests.post(self._base_url, json={
            'cmd': 'dummies.create_dummy',
            'dummy': DUMMY1.to_dict()
        })

        dummy1 = Dummy(**res.json())

        assert dummy1 is not None
        assert dummy1.content, DUMMY1.content
        assert dummy1.key, DUMMY1.key

        # Create another dummy
        res = requests.post(self._base_url, json={
            'cmd': 'dummies.create_dummy',
            'dummy': DUMMY2.to_dict()
        })

        dummy2 = Dummy(**res.json())

        assert dummy2 is not None
        assert dummy2.content, DUMMY2.content
        assert dummy2.key, DUMMY2.key

        # Get all dummies
        res = requests.post(self._base_url,
                            json={
                                'cmd': 'dummies.get_dummies',
                                'filter': FilterParams(),
                                'paging': PagingParams().to_json()
                            })

        assert len(res.json()['data']) >= 2

        # Update the dummy
        dummy1.content = 'Updated Content 1'
        res = requests.post(self._base_url, json={
            'cmd': 'dummies.update_dummy',
            'dummy': dummy1.to_dict()
        })

        updated_dummy1 = Dummy(**res.json())
        assert updated_dummy1.id == dummy1.id
        assert updated_dummy1.content == dummy1.content
        assert updated_dummy1.key == dummy1.key
        dummy1 = updated_dummy1

        # Delete dummy
        res = requests.post(self._base_url, json={
            'cmd': 'dummies.delete_dummy',
            'dummy_id': dummy1.id
        })

        deleted = Dummy(**res.json())
        assert deleted.id == dummy1.id
        assert deleted.content == dummy1.content
        assert deleted.key == dummy1.key

        res = requests.post(self._base_url, json={
            'cmd': 'dummies.get_dummy_by_id',
            'dummy_id': dummy1.id
        })

        assert res.text == ''

        # Failed validation
        res = requests.post(self._base_url, json={
            'cmd': 'dummies.create_dummy',
            'dummy': None
        })

        assert res.json()['code'] == 'INVALID_DATA'
