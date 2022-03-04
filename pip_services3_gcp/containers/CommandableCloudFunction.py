# -*- coding: utf-8 -*-
import flask

from pip_services3_commons.commands import CommandSet, ICommandable
from pip_services3_commons.convert import JsonConverter
from pip_services3_commons.run import Parameters
from pip_services3_rpc.services import HttpResponseSender

from .CloudFunction import CloudFunction
from .CloudFunctionRequestHelper import CloudFunctionRequestHelper


class CommandableCloudFunction(CloudFunction):
    """
    Abstract Google Function function, that acts as a container to instantiate and run components
    and expose them via external entry point. All actions are automatically generated for commands
    defined in :class:`ICommandable <pip_services3_commons.commands.ICommandable.ICommandable>` components.
    Each command is exposed as an action defined by "cmd" parameter.

    Container configuration for this Google Function is stored in `"./config/config.yml"` file.
    But this path can be overridden by `CONFIG_PATH` environment variable.

    Note: This component has been deprecated. Use CloudFunctionService instead.

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`        (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:service:gcp-function:*:1.0`      (optional) :class:`ICounters <pip_services3_gcp.services.iCloudFunctionservice.iCloudFunctionservice>` services to handle action requests
        - `*:service:commandable-gcp-function:*:1.0` (optional) :class:`ICounters <pip_services3_gcp.services.iCloudFunctionservice.iCloudFunctionservice>` services to handle action requests

    Example:

    .. code-block:: python
        class MyCloudFunction(CommandableCloudFunction):
            def __init__(self):
                super().__init__("mygroup", "MyGroup CloudFunction")
                self.__dependency_resolver.put("controller", Descriptor("mygroup","controller","*","*","1.0"))


        cloud_function = MyCloudFunction()
        service.run()
        print("MyCloudFunction is started")

    """

    def __init__(self, name: str = None, description: str = None):
        """
        Creates a new instance of this Google Function.

        :param name: (optional) a container name (accessible via ContextInfo)
        :param description: (optional) a container description (accessible via ContextInfo)
        """
        super(CommandableCloudFunction, self).__init__(name, description)

    def _get_parameters(self, req: flask.Request) -> Parameters:
        """
        Returns body from Google Function request.
        This method can be overloaded in child classes

        :param req: Googl Function request
        :return: Returns Parameters from request
        """
        return CloudFunctionRequestHelper.get_parameters(req)

    def __register_command_set(self, command_set: CommandSet):
        commands = command_set.get_commands()
        for i in range(len(commands)):
            command = commands[i]

            def wrapper(command):
                # wrapper for passing context
                def action(req: flask.Request):
                    correlation_id = self._get_correlation_id(req)
                    args = self._get_parameters(req)
                    timing = self._instrument(correlation_id, self._info.name + '.' + command.get_name())

                    try:
                        result = command.execute(correlation_id, args)
                        timing.end_timing()
                        if isinstance(result, (dict, list, tuple, str, bytes, float, int)):
                            return result
                        else:
                            JsonConverter.to_json(result)
                    except Exception as e:
                        timing.end_timing(e)
                        raise e

                return action

            self._register_action(command.get_name(), None, wrapper(command))

    def register(self):
        """
        Registers all actions in this Google Function.
        """
        controller: ICommandable = self._dependency_resolver.get_one_required('controller')
        command_set = controller.get_command_set()
        self.__register_command_set(command_set)
