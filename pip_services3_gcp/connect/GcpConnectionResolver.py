# -*- coding: utf-8 -*-
from typing import Optional, List
from urllib3.util import url

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.refer import IReferenceable, IReferences, References
from pip_services3_components.auth import CredentialResolver
from pip_services3_components.connect import ConnectionResolver

from pip_services3_gcp.connect.GcpConnectionParams import GcpConnectionParams


class GcpConnectionResolver(IConfigurable, IReferenceable):
    """
    Helper class to retrieve Google connection and credential parameters,
    validate them and compose a :class:`GcpConnectionParams <pip_services3_gcp.connect.GcpConnectionParams.GcpConnectionParams>` value.

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
            - auth_token:    Google-generated ID token or null if using custom auth (IAM)

    ### References ###
        - `*:credential-store:*:*:1.0`  (optional) Credential stores to resolve credentials

    See: :class:`ConnectionParams <pip_services3_components.connect.ConnectionParams.ConnectionParams>` (in the Pip.Services components package)

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

        connection_resolver = GcpConnectionResolver()
        connection_resolver.configure(config)
        connection_resolver.set_references(references)

        connection_params = connection_resolver.resolve("123")

    """

    def __init__(self):
        # The connection resolver.
        self._connection_resolver: ConnectionResolver = ConnectionResolver()
        # The credential resolver.
        self._credential_resolver: CredentialResolver = CredentialResolver()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._connection_resolver.configure(config)
        self._credential_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._connection_resolver.set_references(references)
        self._credential_resolver.set_references(references)

    def resolve(self, correlation_id: Optional[str]):
        """
        Resolves connection and credential parameters and generates a single
        GcpConnectionParams value.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: GcpConnectionParams value or error.
        """
        connection = GcpConnectionParams()

        connection_params = self._connection_resolver.resolve(correlation_id)
        connection.append(connection_params)

        credential_params = self._credential_resolver.lookup(correlation_id)
        connection.append(credential_params)

        # Perform validation
        connection.validate(correlation_id)

        connection = self.__compose_connection(connection)

        return connection

    def __compose_connection(self, connection: GcpConnectionParams) -> GcpConnectionParams:
        connection = GcpConnectionParams.merge_configs(connection)

        uri = connection.get_uri()
        if uri in ['', None]:
            protocol = connection.get_protocol()
            function_name = connection.get_function()
            project_id = connection.get_project_id()
            region = connection.get_region()
            # https://YOUR_REGION-YOUR_PROJECT_ID.cloudfunctions.net/FUNCTION_NAME
            uri = f'{protocol}://{region}-{project_id}.cloudfunctions.net/{function_name or ""}'

            connection.set_uri(uri)
        else:
            address = url.parse_url(uri)
            protocol = address.scheme
            function_name = '' if not address.path else address.path.replace('/', '')
            region, project_id = self.__get_region_and_project_id(uri)

            connection.set_region(region)
            connection.set_project_id(project_id)
            connection.set_function(function_name)
            connection.set_protocol(protocol)

        return connection

    def __get_region_and_project_id(self, uri: str) -> List[str]:
        region_project_id = uri.split('//', 1)[1]
        if region_project_id.count('.') > 1:
            region_project_id = region_project_id.split('.', 1)[0]
            region_project_id = region_project_id.split('-')
        else:
            region_project_id = ['', '']

        return region_project_id
