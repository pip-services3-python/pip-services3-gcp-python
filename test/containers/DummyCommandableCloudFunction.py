# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor

from pip_services3_gcp.containers import CommandableCloudFunction
from ..DummyFactory import DummyFactory


class DummyCommandableCloudFunction(CommandableCloudFunction):
    def __init__(self):
        super(DummyCommandableCloudFunction, self).__init__("dummy", "Dummy cloud function")
        self._dependency_resolver.put('controller',
                                      Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))
        self._factories.add(DummyFactory())
