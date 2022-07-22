# -*- coding: utf-8 -*-
from typing import Any, Optional

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import StringValueMap
from pip_services3_commons.errors import ConfigException
from pip_services3_components.auth import CredentialParams
from pip_services3_components.connect import ConnectionParams


class GcpConnectionParams(ConfigParams):
    """
    Contains connection parameters to authenticate against Google
    and connect to specific Google Cloud Platform.

    The class is able to compose and parse Google Cloud Platform connection parameters.

    ### Configuration parameters ###
        - connections:
            - uri:           full connection uri with specific app and function name
            - protocol:      connection protocol
            - project_id:    is your Google Cloud Platform project ID
            - region:        is the region where your function is deployed
            - function:      is the name of the HTTP function you deployed
            - org_id:        organization name
        - credentials:
            - account: the service account name
            - auth_token:    Google-generated ID token or None if using custom auth (IAM)

    In addition to standard parameters :class:`CredentialParams <pip_services3_components.auth.CredentialParams.CredentialParams>` may contain any number of custom parameters

    See: :class:`GcpConnectionResolver <pip_services3_gcp.connect.GcpConnectionResolver.GcpConnectionResolver>`

    Example:

    .. code-block:: python

        connection = GcpConnectionParams.from_tuples(
            'connection.uri', 'http://east-my_test_project.cloudfunctions.net/myfunction',
            'connection.protocol', 'http',
            'connection.region', 'east',
            'connection.function', 'myfunction',
            'connection.project_id', 'my_test_project',
            'credential.auth_token', '1234',
        )

        uri = connection.get_uri()            # Result: 'http://east-my_test_project.cloudfunctions.net/myfunction'
        region = connection.get_region()               # Result: 'east'
        protocol = connection.get_protocol()           # Result: 'http'
        functionName = connection.get_function()  # Result: 'myfunction'
        projectId = connection.get_project_id()        # Result: 'my_test_project'
        authToken = connection.get_auth_token()        # Result: '123'

    """

    def __init__(self, values: Any = None):
        """
        Creates an new instance of the connection parameters.

        :param values: (optional) an object to be converted into key-value pairs to initialize this connection.
        """
        super(GcpConnectionParams, self).__init__(values)

    def get_protocol(self) -> Optional[str]:
        """
        Gets the Google Platform service connection protocol.

        :return: the Google service connection protocol.
        """
        return super().get_as_nullable_string('protocol')

    def set_protocol(self, value: str):
        """
        Sets the Google Platform service connection protocol.

        :param value: a new Google function connection protocol.
        """
        super().put('protocol', value)

    def get_uri(self) -> Optional[str]:
        """
        Gets the Google Platform service uri.

        :return: the Google service uri.
        """
        return super().get_as_nullable_string('uri')

    def set_uri(self, value: str):
        """
        Sets the Google Platform service uri.

        :param: a new Google service uri.
        """
        super().put('uri', value)

    def get_function(self) -> Optional[str]:
        """
        Gets the Google Platform service name.

        :return: the Google service name.
        """
        return super().get_as_nullable_string('function')

    def set_function(self, value: str):
        """
        Sets the Google function name.

        :param: the Google function name.
        """
        super().put('function', value)

    def get_region(self) -> Optional[str]:
        """
        Gets the region where your function is deployed.

        :return: the region of deployed function.
        """
        return super().get_as_nullable_string('region')

    def set_region(self, value: str):
        """
        Sets the region where your function is deployed.

        :param: the region of deployed function.
        """
        super().put('region', value)

    def get_project_id(self) -> Optional[str]:
        """
        Gets the Google Cloud Platform project ID.

        :return: the project ID.
        """
        return super().get_as_nullable_string('project_id')

    def set_project_id(self, value: str):
        """
        Sets the Google Cloud Platform project ID.

        :param: the project ID.
        """
        super().put('project_id', value)

    def get_auth_token(self) -> Optional[str]:
        """
        Gets an ID token with the request to authenticate themselves

        :return: the ID token.
        """
        return super().get_as_nullable_string('auth_token')

    def set_auth_token(self, value: str):
        """
        Sets an ID token with the request to authenticate themselves

        :param: a new ID token.
        """
        super().put('auth_token', value)

    def get_account(self) -> Optional[str]:
        """
        Gets the service account name

        :return: the account name.
        """
        return super().get_as_nullable_string('account')

    def set_account(self, value: str):
        """
        Sets the service account name

        :param: a new account name.
        """
        super().put('account', value)

    def get_org_id(self) -> Optional[str]:
        """
        Gets organization name

        :return: the organization name.
        """
        return super().get_as_nullable_string('org_id')

    def set_org_id(self, value: str):
        """
        Sets organization name

        :param: a new organization name.
        """
        super().put('org_id', value)

    def validate(self, correlation_id: Optional[str]):
        """
        Validates this connection parameters

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        uri = self.get_uri()
        protocol = self.get_protocol()
        function_name = self.get_function()
        region = self.get_region()
        project_id = self.get_project_id()

        if uri is None and None in [project_id, region, function_name, protocol]:
            raise ConfigException(
                correlation_id,
                "NO_CONNECTION_URI",
                "No uri, project_id, region and function is configured in Google function uri"
            )

        if protocol is not None and 'http' != protocol and 'https' != protocol:
            raise ConfigException(
                correlation_id,
                "WRONG_PROTOCOL", "Protocol is not supported by REST connection"
            ).with_details('protocol', protocol)

    @staticmethod
    def from_string(line: str) -> 'GcpConnectionParams':
        """
        Creates a new GcpConnectionParams object filled with key-value pairs serialized as a string.

        :param line: a string with serialized key-value pairs as "key1=value1;key2=value2;..."
        Example: "Key1=123;Key2=ABC;Key3=2016-09-16T00:00:00.00Z"

        :return: a new GcpConnectionParams object.
        """
        map = StringValueMap.from_string(line)
        return GcpConnectionParams(map)

    @staticmethod
    def from_config(config: ConfigParams) -> 'GcpConnectionParams':
        """
        Retrieves GcpConnectionParams from configuration parameters.
        The values are retrieves from "connection" and "credential" sections.

        :param config: configuration parameters
        :return: the generated GcpConnectionParams object.
        """
        result = GcpConnectionParams()

        credentials = CredentialParams.from_config(config)
        for credential in credentials:
            result.append(credential)

        connections = ConnectionParams.from_config(config)
        for connection in connections:
            result.append(connection)

        return result

    @staticmethod
    def merge_configs(*configs: 'ConfigParams') -> 'GcpConnectionParams':
        """
        Retrieves GcpConnectionParams from multiple configuration parameters.
        The values are retrieves from "connection" and "credential" sections.

        :param configs: a set with configuration parameters
        :return: the generated GcpConnectionParams object.
        """
        config = ConfigParams.merge_configs(*configs)
        return GcpConnectionParams(config)

    @staticmethod
    def from_tuples(*tuples: Any) -> 'GcpConnectionParams':
        """
        Creates a new ConfigParams object filled with provided key-args pairs called tuples.
        Tuples parameters contain a sequence of key1, value1, key2, value2, ... pairs.

        :param tuples: the tuples to fill a new ConfigParams object.

        :return: a new ConfigParams object.
        """

        config = ConfigParams.from_tuples(*tuples)
        return GcpConnectionParams.from_config(config)
