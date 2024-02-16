"""
Hench
"""

import abc


class AbstractStep(abc.ABC):
    """Base step type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @abc.abstractmethod
    def __call__(self):
        "Force implement function"

        raise NotImplementedError("Step.__call__ not implemented.")


class AbstractTask(abc.ABC):
    """Base task type"""

    def __init__(self, steps: list[AbstractStep] = None) -> None:
        """Constructor"""

        self._name = type(self).__name__

        self._steps: list[AbstractStep] = (
            steps if steps and self.__validate(steps) else []
        )

    @staticmethod
    def __validate(steps: list[AbstractStep]) -> bool:
        if not all([isinstance(step, AbstractStep) for step in steps]):
            raise TypeError("Unsupported step found.")

        return True

    @abc.abstractmethod
    def execute(self):
        """Execute a task"""


class AbstractWorkflow(abc.ABC):
    """Base workflow type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @abc.abstractmethod
    def execute(self):
        """Execute a workflow"""
