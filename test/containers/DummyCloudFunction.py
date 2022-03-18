# -*- coding: utf-8 -*-
import flask
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.refer import Descriptor, IReferences
from pip_services3_commons.validate import ObjectSchema, FilterParamsSchema, PagingParamsSchema

from pip_services3_gcp.containers import CloudFunction
from ..Dummy import Dummy
from ..DummyFactory import DummyFactory
from ..DummySchema import DummySchema
from ..IDummyController import IDummyController


class DummyCloudFunction(CloudFunction):
    def __init__(self):
        super(DummyCloudFunction, self).__init__("dummy", "Dummy cloud function")
        self._dependency_resolver.put('controller',
                                      Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))

        self._controller: IDummyController = None
        self._factories.add(DummyFactory())

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._controller = self._dependency_resolver.get_one_required('controller')

    def __get_page_by_filter(self, req: flask.Request):
        params = req.get_json()

        page = self._controller.get_page_by_filter(
            self._get_correlation_id(req),
            FilterParams(params.get('filter', {})),
            PagingParams(params.get('paging'))
        )

        if len(page.data) > 0:
            serealized_items = []
            for item in page.data:
                serealized_items.append(item.to_dict())

            page = page.to_json()
            page['data'] = serealized_items

        return page

    def __get_one_by_id(self, req: flask.Request):
        params = req.get_json()

        dummy = self._controller.get_one_by_id(
            self._get_correlation_id(req),
            params.get('dummy_id')
        )

        if dummy:
            return dummy.to_dict()
        else:
            return '', 204

    def __create(self, req: flask.Request):
        params = req.get_json()

        dummy = self._controller.create(
            self._get_correlation_id(req),
            Dummy(**params.get('dummy'))
        )

        return dummy.to_dict()

    def __update(self, req: flask.Request):
        params = req.get_json()

        dummy = self._controller.update(
            self._get_correlation_id(req),
            Dummy(**params.get('dummy'))
        )

        return dummy.to_dict()

    def __delete_by_id(self, req: flask.Request):
        params = req.get_json()

        dummy = self._controller.delete_by_id(
            self._get_correlation_id(req),
            params.get('dummy_id')
        )

        if dummy:
            return dummy.to_dict()
        else:
            return '', 204

    def register(self):
        self._register_action(
            'get_dummies',
            ObjectSchema(True).with_optional_property('body',
                ObjectSchema(True)
                    .with_optional_property('filter', FilterParamsSchema())
                    .with_optional_property('paging', PagingParamsSchema())
            ),
            self.__get_page_by_filter
        )

        self._register_action(
            'get_dummy_by_id',
            ObjectSchema(True).with_optional_property('body',
                ObjectSchema(True).with_optional_property('dummy_id', TypeCode.String)
            ),
            self.__get_one_by_id
        )

        self._register_action(
            'create_dummy',
            ObjectSchema(True).with_optional_property('body',
                ObjectSchema(True).with_required_property('dummy', DummySchema())
            ),
            self.__create
        )

        self._register_action(
            'update_dummy',
            ObjectSchema(True).with_optional_property('body',
                ObjectSchema(True).with_required_property('dummy', DummySchema())
            ),
            self.__update
        )

        self._register_action(
            'delete_dummy',
            ObjectSchema(True).with_optional_property('body',
                ObjectSchema(True).with_required_property('dummy_id', TypeCode.String)
            ),
            self.__delete_by_id
        )
