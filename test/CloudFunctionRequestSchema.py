# -*- coding: utf-8 -*-
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.validate import ObjectSchema


class CloudFunctionRequestSchema(ObjectSchema):
    def __init__(self):
        super(CloudFunctionRequestSchema, self).__init__()

        self.with_optional_property('body', TypeCode.Map)
        self.with_optional_property('query', TypeCode.Map)
