# -*- coding: utf-8 -*-

from pip_services3_commons.config import ConfigParams

from pip_services3_gcp.connect import GcpConnectionResolver
from pip_services3_gcp.connect.GcpConnectionParams import GcpConnectionParams


class TestGcpConnectionParams:

    def test_empty_connection(self):
        connection = GcpConnectionParams()
        assert connection.get_account() is None
        assert connection.get_region() is None
        assert connection.get_project_id() is None
        assert connection.get_function() is None
        assert connection.get_protocol() is None
        assert connection.get_org_id() is None
        assert connection.get_auth_token() is None

    def test_compose_config(self):
        config1 = ConfigParams.from_tuples(
            'connection.uri', 'http://east-my_test_project.cloudfunctions.net/myfunction',
            'credential.auth_token', '1234',
        )

        config2 = ConfigParams.from_tuples(
            'connection.protocol', 'http',
            'connection.region', 'east',
            'connection.function', 'myfunction',
            'connection.project_id', 'my_test_project',
            'credential.auth_token', '1234',
        )
        resolver = GcpConnectionResolver()
        resolver.configure(config1)
        connection = resolver.resolve(None)

        assert 'http://east-my_test_project.cloudfunctions.net/myfunction' == connection.get_uri()
        assert 'east' == connection.get_region()
        assert 'http' == connection.get_protocol()
        assert 'myfunction' == connection.get_function()
        assert 'my_test_project' == connection.get_project_id()
        assert '1234' == connection.get_auth_token()

        resolver = GcpConnectionResolver()
        resolver.configure(config2)
        connection = resolver.resolve(None)

        assert 'http://east-my_test_project.cloudfunctions.net/myfunction' == connection.get_uri()
        assert 'east' == connection.get_region()
        assert 'http' == connection.get_protocol()
        assert 'myfunction' == connection.get_function()
        assert 'my_test_project' == connection.get_project_id()
        assert '1234' == connection.get_auth_token()
