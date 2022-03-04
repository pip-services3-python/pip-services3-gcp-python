# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from .DummyController import DummyController

from .services.DummyCloudFunctionService import DummyCloudFunctionService
from .services.DummyCommandableCloudFunctionService import DummyCommandableCloudFunctionService


class DummyFactory(Factory):
    DescriptorDummy = Descriptor("pip-services-dummies", "factory", "default", "default", "1.0")
    ControllerDescriptor = Descriptor("pip-services-dummies", "controller", "default", "*", "1.0")
    CloudFunctionServiceDescriptor = Descriptor("pip-services-dummies", "service", "gcp-function", "*", "1.0")
    CmdCloudFunctionServiceDescriptor = Descriptor("pip-services-dummies", "service", "commandable-gcp-function", "*",
                                                   "1.0")

    def __init__(self):
        super().__init__()
        self.register_as_type(DummyFactory.ControllerDescriptor, DummyController)
        self.register_as_type(DummyFactory.CloudFunctionServiceDescriptor, DummyCloudFunctionService)
        self.register_as_type(DummyFactory.CmdCloudFunctionServiceDescriptor, DummyCommandableCloudFunctionService)
