# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

import flask
from pip_services3_commons.validate import Schema


class CloudFunctionAction:

    def __init__(self, cmd: str = None, schema: Optional[Schema] = None, action: Callable[[flask.Request], None] = None):
        # Command to call the action
        self.cmd: str = cmd

        # Schema to validate action parameters
        self.schema: Optional[Schema] = schema

        self.action = action if action else self.action

    def action(self, request: flask.Request) -> Any:
        """
        Action to be executed
        """
