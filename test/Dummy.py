# -*- coding: utf-8 -*-
from typing import Optional

from pip_services3_commons.data import IStringIdentifiable


class Dummy(IStringIdentifiable):

    def __init__(self, id: Optional[str], key: str, content: str):
        self.id = id
        self.key = key
        self.content = content

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'key': self.key,
            'content': self.content
        }
