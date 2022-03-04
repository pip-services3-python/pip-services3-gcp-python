# -*- coding: utf-8 -*-
from typing import Optional

from pip_services3_commons.data import FilterParams, PagingParams, DataPage

from pip_services3_gcp.clients.CloudFunctionClient import CloudFunctionClient
from test.Dummy import Dummy
from test.IDummyClient import IDummyClient


class DummyCloudFunctionClient(CloudFunctionClient, IDummyClient):
    def get_dummies(self, correlation_id: Optional[str], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        response = self._call('dummies.get_dummies', correlation_id, {
            'filter': filter_params,
            'paging': paging.to_json()
        })

        page = DataPage([], response.get('total'))

        if response.get('data'):
            for item in response['data']:
                page.data.append(Dummy(**item))

        return page

    def get_dummy_by_id(self, correlation_id: Optional[str], dummy_id: str) -> Optional[Dummy]:
        response = self._call('dummies.get_dummy_by_id', correlation_id, {'dummy_id': dummy_id})

        if response is None or len(response.keys()) == 0:
            return None

        return Dummy(**response)

    def create_dummy(self, correlation_id: Optional[str], dummy: Dummy) -> Dummy:
        response = self._call('dummies.create_dummy', correlation_id, {'dummy': dummy.to_dict()})

        if response:
            return Dummy(**response)

    def update_dummy(self, correlation_id: Optional[str], dummy: Dummy) -> Dummy:
        response = self._call('dummies.update_dummy', correlation_id, {'dummy': dummy.to_dict()})

        if response:
            return Dummy(**response)

    def delete_dummy(self, correlation_id: Optional[str], dummy_id: str) -> Dummy:
        response = self._call('dummies.delete_dummy', correlation_id, {'dummy_id': dummy_id})

        if response:
            return Dummy(**response)
