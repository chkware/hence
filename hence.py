"""
Hench
"""

import abc
import typing

from paradag import DAG


class AbstractStep(abc.ABC):
    """Base step type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @abc.abstractmethod
    def __call__(self):
        "Force implement function"

        raise NotImplementedError("Step.__call__ not implemented.")


class Task:
    """Base task type"""

    def __init__(self, steps: list[AbstractStep] = None) -> None:
        """Constructor"""

        self._name = type(self).__name__
        self._dag = DAG()

        self._steps: list[AbstractStep] = (
            steps if steps and self.__validate(steps) else []
        )

        self.__setup_dag()

    @staticmethod
    def __validate(steps: list[AbstractStep]) -> bool:
        """Validate steps are ok"""

        if not all([isinstance(step, AbstractStep) for step in steps]):
            raise TypeError("Unsupported step found.")

        return True

    def __setup_dag(self) -> bool:
        """Setup DAG"""
        self._dag.add_vertex(*self._steps)

        for index in range(1, len(self._steps)):
            self._dag.add_edge(self._steps[index - 1], self._steps[index])

    @typing.final
    def execute(self):
        """Execute a task"""


class Workflow:
    """Base workflow type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @typing.final
    def execute(self):
        """Execute a workflow"""
