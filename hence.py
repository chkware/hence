"""
Hench
"""

import abc


class AbstractStep(abc.ABC):
    """Base step type"""

    @abc.abstractmethod
    def __call__(self):
        "Force implement function"

        raise NotImplementedError("Step.__call__ not implemented.")


class AbstractTask(abc.ABC):
    """Base task type"""

    def __init__(self, steps: list[AbstractStep] = None) -> None:
        """Create instance of Task"""

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
        "Execute a task"


class AbstractWorkflow(abc.ABC):
    """Base workflow type"""

    @abc.abstractmethod
    def execute(self):
        "Execute a workflow"
