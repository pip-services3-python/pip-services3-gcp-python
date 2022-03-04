# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor

from pip_services3_gcp.services import CommandableCloudFunctionService


class DummyCommandableCloudFunctionService(CommandableCloudFunctionService):
    def __init__(self):
        super(DummyCommandableCloudFunctionService, self).__init__('dummies')
        self._dependency_resolver.put('controller', Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))