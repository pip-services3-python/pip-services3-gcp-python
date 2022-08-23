# -*- coding: utf-8 -*-
import flask
from pip_services3_commons.run import Parameters


class CloudFunctionRequestHelper:
    """
    Class that helps to prepare function requests
    """

    @staticmethod
    def get_correlation_id(req: flask.Request) -> str:
        """
        Returns correlationId from Google Function request.

        :param req: the Google Function request
        :return: returns correlationId from request
        """
        correlation_id = req.view_args.get('correlation_id', '')
        try:
            if correlation_id == '' and req.is_json:
                correlation_id = req.json.get('correlation_id', '')
                if correlation_id == '':
                    correlation_id = req.args.get('correlation_id', '')
        except Exception as e:
            # Ignore the error
            pass

        return correlation_id

    @staticmethod
    def get_command(req: flask.Request):
        """
        Returns command from Google Function request.

        :param req: the Google Function request
        :return: returns command from request
        """
        cmd = req.view_args.get('cmd', '')
        try:
            if cmd == '' and req.is_json:
                cmd = req.json.get('cmd', '')
                if cmd == '':
                    cmd = req.args.get('cmd', '')
        except Exception as e:
            # Ignore the error
            pass

        return cmd

    @staticmethod
    def get_parameters(req: flask.Request) -> Parameters:
        """
        Returns body from Google Function request http request.

        :param req: the Google Function request (flask object request)
        :return: returns body from request
        """
        body = req
        try:
            if req.is_json:
                body = req.get_json()
        except Exception as e:
            # Ignore the error
            pass

        return Parameters.from_value(body)
