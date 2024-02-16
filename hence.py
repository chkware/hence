"""
Hench
"""

import abc


class AbstractWorkflow(abc.ABC):
    """Base workflow type"""

    @abc.abstractmethod
    def execute(self):
        "execute"
