# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services3_commons.data import FilterParams, PagingParams, DataPage

from .Dummy import Dummy


class IDummyController(ABC):
    @abstractmethod
    def get_page_by_filter(self, correlation_id: Optional[str], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        pass

    @abstractmethod
    def get_one_by_id(self, correlation_id: Optional[str], id: str) -> Dummy:
        pass

    @abstractmethod
    def create(self, correlation_id: Optional[str], entity: Dummy) -> Dummy:
        pass

    @abstractmethod
    def update(self, correlation_id: Optional[str], new_entity: Dummy) -> Dummy:
        pass

    @abstractmethod
    def delete_by_id(self, correlation_id: Optional[str], id: str) -> Dummy:
        pass
