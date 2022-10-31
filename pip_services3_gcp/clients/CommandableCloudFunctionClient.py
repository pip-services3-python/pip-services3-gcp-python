# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services3_gcp.clients.CloudFunctionClient import CloudFunctionClient


class CommandableCloudFunctionClient(CloudFunctionClient):
    """
    Abstract client that calls commandable Google Cloud Functions.
    Commandable services are generated automatically for :class:`ICommandable <pip_services3_commons.commands.ICommandable.ICommandable>`.
    Each command is exposed as action determined by "cmd" parameter.

    ### Configuration parameters ###
        - connections:
            - uri:           full connection uri with specific app and function name
            - protocol:      connection protocol
            - project_id:    is your Google Cloud Platform project ID
            - region:        is the region where your function is deployed
            - function:      is the name of the HTTP function you deployed
            - org_id:        organization name
        - options:
            - retries:               number of retries (default: 3)
            - connect_timeout:       connection timeout in milliseconds (default: 10 sec)
            - timeout:               invocation timeout in milliseconds (default: 10 sec)
        - credentials:
            - account: the service account name
            - auth_token:    Google-generated ID token or None if using custom auth (IAM)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`         (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` services to resolve connection
        - `*:credential-store:*:*:1.0`  (optional) Credential stores to resolve credentials

    See :class:`CloudFunction <pip_services3_gcp.containers.CloudFunction.CloudFunction>`

    Example:

    .. code-block:: python
        class MyCommandableGoogleClient(CommandableCloudFunctionClient, IMyClient):
            def get_data(self, correlation_id, id) -> MyData:
                timing = self._instrument(correlation_id, 'myclient.get_data')
                result = self.call_command("get_data", correlation_id, {'id': id})

                data = MyData(**result)

                timing.end_timing()
                return data

        client = MyCommandableGoogleClient('mydata')
        client.configure(ConfigParams.from_tuples(
            'connection.uri", "http://region-id.cloudfunctions.net/myfunction',
            'connection.protocol', 'http',
            'connection.region', 'region',
            'connection.function', 'myfunction',
            'connection.project_id', 'id',
            'credential.auth_token', 'XXX',
        ))

        result = client.get_data("123", "1")
    """

    def __init__(self, name: str):
        """
        Creates a new instance of this client.

        :param name: a service name.
        """
        super(CommandableCloudFunctionClient, self).__init__()
        self.__name = name

    def call_command(self, cmd: str, correlation_id: Optional[str], params: dict) -> Any:
        """
        Calls a remote action in Google Function.
        The name of the action is added as "cmd" parameter
        to the action parameters.

        :param cmd: an action name
        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param params: command parameters.
        :return: action result.
        """
        timing = self._instrument(correlation_id, self.__name + '.' + cmd)
        try:
            result = self._call(cmd, correlation_id, params)
            timing.end_timing()
            return result
        except Exception as err:
            timing.end_timing(err)
            raise err
