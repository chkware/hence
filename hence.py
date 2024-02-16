"""
Hench
"""

import abc


class AbstractWorkflow(abc.ABC):
    """Base workflow type"""

    @abc.abstractmethod
    def execute(self):
        "execute"


class AbstractTask(abc.ABC):
    """Base task type"""

    @abc.abstractmethod
    def execute(self):
        "execute"


class AbstractStep(abc.ABC):
    """Base step type"""

    @abc.abstractmethod
    def __call__(self):
        "execute"
