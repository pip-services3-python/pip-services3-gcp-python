# -*- coding: utf-8 -*-
from typing import List, Optional

from pip_services3_commons.commands import ICommandable, CommandSet
from pip_services3_commons.data import FilterParams, PagingParams, DataPage, IdGenerator

from .Dummy import Dummy
from .DummyCommandSet import DummyCommandSet
from .IDummyController import IDummyController


class DummyController(IDummyController, ICommandable):

    def __init__(self):
        self.__command_set: DummyCommandSet = None
        self.__entities: List[Dummy] = []

    def get_command_set(self) -> CommandSet:
        if self.__command_set is None:
            self.__command_set = DummyCommandSet(self)
        return self.__command_set

    def get_page_by_filter(self, correlation_id: Optional[str], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        filter = filter_params if filter_params is not None else None
        key = filter.get_as_nullable_string("key")

        paging = paging if paging is not None else PagingParams()
        skip: int = paging.get_skip(0)
        take: int = paging.get_take(100)

        result: List[Dummy] = []
        for i in range(len(self.__entities)):
            entity = self.__entities[i]
            if key is not None and key != entity.key:
                continue

            skip -= 1
            if skip >= 0:
                continue

            take -= 1
            if take < 0:
                break

            result.append(entity)

        return DataPage(result)

    def get_one_by_id(self, correlation_id: Optional[str], id: str) -> Optional[Dummy]:
        for entity in self.__entities:
            if id == entity.id:
                return entity

        return None

    def create(self, correlation_id: Optional[str], entity: Dummy) -> Dummy:
        if entity.id is None:
            entity.id = IdGenerator.next_long()
            self.__entities.append(entity)

        return entity

    def update(self, correlation_id: Optional[str], new_entity: Dummy) -> Optional[Dummy]:
        for index in range(len(self.__entities)):
            entity = self.__entities[index]
            if entity.id == new_entity.id:
                self.__entities[index] = new_entity
                return new_entity

        return None

    def delete_by_id(self, correlation_id: Optional[str], id: str) -> Optional[Dummy]:
        for index in range(len(self.__entities)):
            entity = self.__entities[index]
            if entity.id == id:
                del self.__entities[index]
                return entity

        return None
