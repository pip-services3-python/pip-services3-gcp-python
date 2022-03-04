# -*- coding: utf-8 -*-
from pip_services3_commons.config import ConfigParams

from test.services.DummyCloudFunction import DummyCloudFunction
from test.services.DummyCommandableCloudFunction import DummyCommandableCloudFunction

commandable_function_service = None


def commandable_handler(req):
    global commandable_function_service

    config = ConfigParams.from_tuples(
        'logger.descriptor', 'pip-services:logger:console:default:1.0',
        'controller.descriptor', 'pip-services-dummies:controller:default:default:1.0',
        'service.descriptor', 'pip-services-dummies:service:commandable-gcp-function:default:1.0'
    )

    if commandable_function_service is None:
        commandable_function_service = DummyCommandableCloudFunction()
        commandable_function_service.configure(config)
        commandable_function_service.open(None)

    function_handler = commandable_function_service.get_handler()

    return function_handler(req)


# CloudFunctionService
function_service = None


def handler(req):
    global function_service

    config = ConfigParams.from_tuples(
        'logger.descriptor', 'pip-services:logger:console:default:1.0',
        'controller.descriptor', 'pip-services-dummies:controller:default:default:1.0',
        'service.descriptor', 'pip-services-dummies:service:gcp-function:default:1.0'
    )

    if function_service is None:
        function_service = DummyCloudFunction()
        function_service.configure(config)
        function_service.open(None)

    function_handler = function_service.get_handler()

    return function_handler(req)
