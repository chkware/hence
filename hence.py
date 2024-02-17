"""
Hench
"""

import abc
import typing

from paradag import DAG, SequentialProcessor, dag_run


class AbstractWork(abc.ABC):
    """Base work type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @abc.abstractmethod
    def __call__(self):
        "Force implement function"

        raise NotImplementedError("__call__ not implemented.")


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


class WorkGroup(DagExecutor):
    """Collection of Work"""

    def __init__(self, works: list[AbstractWork] = None) -> None:
        """Constructor"""

        super().__init__()

        self._name = type(self).__name__

        self._works: list[AbstractWork] = (
            works if works and self.__validate(works) else []
        )

        self.setup_dag()

    @staticmethod
    def __validate(works: list[AbstractWork]) -> bool:
        """Validate works are ok"""

        if not all([isinstance(work, AbstractWork) for work in works]):
            raise TypeError("Unsupported work found.")

        return True

    @property
    def vertices(self) -> list[AbstractWork]:
        return self._works if self._works else []


class Workflow(DagExecutor):
    """Base workflow type"""

    def __init__(self, work_groups: list[WorkGroup] = None) -> None:
        """Constructor"""

        super().__init__()

        self._name = type(self).__name__

        self._work_groups: list[WorkGroup] = (
            work_groups if work_groups and self.__validate(work_groups) else []
        )

        self.setup_dag()

    @property
    def vertices(self) -> list[WorkGroup]:
        return self._work_groups if self._work_groups else []

    @staticmethod
    def __validate(work_groups: list[WorkGroup]) -> bool:
        """Validate tasks are ok"""

        if not all([isinstance(work_group, WorkGroup) for work_group in work_groups]):
            raise TypeError("Unsupported workgroup found.")

        return True


class LinearExecutor:
    """Linear executor"""

    def param(self, vertex: typing.Any) -> typing.Any:
        """Selecting parameters"""

        return vertex

    def execute(self, work: typing.Any) -> typing.Any:
        """Execute"""

        if isinstance(work, AbstractWork) and callable(work):
            return work()
        elif isinstance(work, WorkGroup):
            return work.execute_dag()
        else:
            raise TypeError(f"Incorrect type of `work`: {type(work)} found.")
