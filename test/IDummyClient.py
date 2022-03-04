# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services3_commons.data import FilterParams, PagingParams, DataPage

from test.Dummy import Dummy


class IDummyClient(ABC):
    @abstractmethod
    def get_dummies(self, correlation_id: Optional[str], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        pass

    @abstractmethod
    def get_dummy_by_id(self, correlation_id: Optional[str], dummy_id: str) -> Dummy:
        pass

    @abstractmethod
    def create_dummy(self, correlation_id: Optional[str], dummy: Dummy) -> Dummy:
        pass

    @abstractmethod
    def update_dummy(self, correlation_id: Optional[str], dummy: Dummy) -> Dummy:
        pass

    @abstractmethod
    def delete_dummy(self, correlation_id: Optional[str], dummy_id: str) -> Dummy:
        pass
