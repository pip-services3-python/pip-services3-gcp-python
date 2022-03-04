# -*- coding: utf-8 -*-
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.validate import ObjectSchema


class DummySchema(ObjectSchema):

    def __init__(self):
        super(DummySchema, self).__init__()

        self.with_optional_property('id', TypeCode.String)
        self.with_required_property('key', TypeCode.String)
        self.with_optional_property('content', TypeCode.String)
