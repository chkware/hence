"""
Hench
"""

import abc
import typing

from paradag import DAG, SequentialProcessor, dag_run


class AbstractStep(abc.ABC):
    """Base step type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @abc.abstractmethod
    def __call__(self):
        "Force implement function"

        raise NotImplementedError("Step.__call__ not implemented.")


class DagExecutor:
    """DagExecutor"""

    def __init__(self) -> None:
        """DagExecutor constructor"""

        self._dag = DAG()

    @property
    @abc.abstractproperty
    def vertices(self) -> list[typing.Any]:
        """Get unit_of_works"""

    @typing.final
    def setup_dag(self) -> bool:
        """Setup DAG"""

        self._dag.add_vertex(*self.vertices)

        for index in range(1, len(self.vertices)):
            self._dag.add_edge(self.vertices[index - 1], self.vertices[index])

    @typing.final
    def execute_dag(self) -> list[typing.Any]:
        """Execute the dag"""

        resp = dag_run(
            self._dag, processor=SequentialProcessor(), executor=LinearExecutor()
        )

        return resp


class Task(DagExecutor):
    """Base task type"""

    def __init__(self, steps: list[AbstractStep] = None) -> None:
        """Constructor"""

        super().__init__()

        self._name = type(self).__name__

        self._steps: list[AbstractStep] = (
            steps if steps and self.__validate(steps) else []
        )

        self.setup_dag()

    @staticmethod
    def __validate(steps: list[AbstractStep]) -> bool:
        """Validate steps are ok"""

        if not all([isinstance(step, AbstractStep) for step in steps]):
            raise TypeError("Unsupported step found.")

        return True

    @property
    def vertices(self) -> list[AbstractStep]:
        return self._steps if self._steps else []


class Workflow:
    """Base workflow type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @typing.final
    def execute(self):
        """Execute a workflow"""


class LinearExecutor:
    """Linear executor"""

    def param(self, vertex: typing.Any) -> typing.Any:
        """Selecting parameters"""

        return vertex

    def execute(self, step: typing.Any) -> typing.Any:
        """Execute"""

        if isinstance(step, AbstractStep):
            return step()
        else:
            raise TypeError(f"Incorrect type of `step`: {type(step)} found.")
