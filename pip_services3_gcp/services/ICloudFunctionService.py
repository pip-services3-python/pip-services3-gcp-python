# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List

from .CloudFunctionAction import CloudFunctionAction


class ICloudFunctionService(ABC):
    """
    An interface that allows to integrate Google Function services into Google Function containers
    and connect their actions to the function calls.
    """

    @abstractmethod
    def get_actions(self) -> List[CloudFunctionAction]:
        """
        Get all actions supported by the service.

        :return: an array with supported actions.
        """
        pass
