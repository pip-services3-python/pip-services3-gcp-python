# -*- coding: utf-8 -*-
import json
import flask

from typing import Any, Union

from pip_services3_commons.data import DataPage
from pip_services3_commons.convert import JsonConverter
from pip_services3_commons.commands import CommandSet, ICommandable
from pip_services3_commons.run import Parameters

from pip_services3_gcp.containers import CloudFunctionRequestHelper
from pip_services3_gcp.services import CloudFunctionService


class CommandableCloudFunctionService(CloudFunctionService):
    """
    Abstract service that receives commands via Google Function protocol
    to operations automatically generated for commands defined in :class:`ICommandable <pip_services3_commons.commands.ICommandable.ICommandable>`.
    Each command is exposed as invoke method that receives command name and parameters.

    Commandable services require only 3 lines of code to implement a robust external
    Google Function-based remote interface.

    This service is intended to work inside Google Function container that
    exploses registered actions externally.

    ### Configuration parameters ###
        - dependencies:
            - controller:            override for Controller dependency

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements

    Example:

    .. code-block:: python

            class MyCommandableCloudFunctionService(CommandableCloudFunctionService):
                def __init__(self):
                    super().__init__("mydata")
                    self._dependency_resolver.put(
                        "controller",
                        Descriptor("mygroup","controller","*","*","1.0")
                  )

            service = MyCommandableCloudFunctionService()
            service.set_references(References.from_tuples(
                Descriptor("mygroup","controller","default","default","1.0"), controller
            ))

            service.open("123")
            print("The Google Function service is running")

    """

    def __init__(self, name: str):
        """
        Creates a new instance of the service.

        :param name: a service name.
        """
        super().__init__(name)
        self._dependency_resolver.put('controller', 'none')

        self.__command_set: CommandSet = None

    def _get_parameters(self, req: flask.Request) -> Parameters:
        """
        Returns body from Google Function request.
        This method can be overloaded in child classes

        :param req: Google Function request
        :return: Parameters from request
        """
        return CloudFunctionRequestHelper.get_parameters(req)

    def register(self):
        """
        Registers all actions in Google Function.
        """

        def wrapper(command):
            # wrapper for passing context
            def action(req: flask.Request):
                correlation_id = self._get_correlation_id(req)

                args = Parameters.from_value({} if not req.is_json else req.get_json())
                if correlation_id:
                    args.remove('correlation_id')

                timing = self._instrument(correlation_id, name)
                try:
                    result = command.execute(correlation_id, args)
                    # Conversion to response data format
                    result = self.__to_response_format(result)
                    timing.end_timing()
                    return result
                except Exception as e:
                    timing.end_failure(e)
                    return self._compose_error(e)

            return action

        controller: ICommandable = self._dependency_resolver.get_one_required('controller')
        self.__command_set = controller.get_command_set()

        commands = self.__command_set.get_commands()
        for index in range(len(commands)):
            command = commands[index]
            name = command.get_name()

            self._register_action(name, None, wrapper(command))

    def __to_response_format(self, res: Any) -> Union[dict, tuple]:
        if res is None:
            return '', 204
        if not isinstance(res, (int, str, dict, tuple, list, bytes, float, flask.Response)):
            if hasattr(res, 'to_dict'):
                res = res.to_dict()
            elif hasattr(res, 'to_json'):
                if isinstance(res, DataPage) and len(res.data) > 0 and not isinstance(res.data[0], dict):
                    res.data = json.loads(JsonConverter.to_json(res.data))
                res = res.to_json()
            else:
                res = JsonConverter.to_json(res)

        return res
