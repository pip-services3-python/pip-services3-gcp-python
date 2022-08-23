# -*- coding: utf-8 -*-
from typing import Any, Callable

import flask
from pip_services3_commons.validate import Schema


class CloudFunctionAction:

    def __init__(self, cmd: str = None, schema: Schema = None, action: Callable[[flask.Request], Any] = None):
        # Command to call the action
        self.cmd: str = cmd

        # Schema to validate action parameters
        self.schema: Schema = schema

        self.action = action if action else self.action

    def action(self, request: flask.Request) -> Any:
        """
        Action to be executed
        """
