"""
Hench
"""

from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from collections import UserList
import functools
from typing import Any, Callable, NamedTuple, final

from paradag import DAG, SequentialProcessor, dag_run


class WorkExecFrame(NamedTuple):
    """WorkFrame holds what goes inside works"""

    work_func: Callable = lambda: ...
    work_exec_output: Any = None
class WorkList(UserList):
    """WorkList"""

    def __init__(self, iterable: list = None):
        """Create"""
        if iterable is None:
            iterable = []

        super().__init__(self._validate_type(item) for item in iterable)

    def __setitem__(self, index, item):
        """Overload set [] to support setting"""

        super().__setitem__(index, self._validate_type(item))

    def append(self, item):
        """Overload append to support append"""

        super().append(self._validate_type(item))

    def _validate_type(self, value):
        if isinstance(value, (WorkExecFrame)):
            return value
        raise TypeError(f"WorkExecFrame expected, got {type(value).__name__}.")

    @classmethod
    def from_works(cls, work_lst: list[AbstractWork]) -> WorkList:
        """create WorkList from a list of AbstractWork"""

        if not all([isinstance(work, AbstractWork) for work in work_lst]):
            raise TypeError("Unsupported work found. AbstractWork expected.")

        return cls(
            [
                WorkExecFrame(title=type(work).__name__, function=work.handle)
                for work in work_lst
            ]
        )


def work(
    title,
    pass_work: bool = False,
    pass_works: bool = False,
    pass_context: bool = False,
    before: Callable = lambda: ...,
    after: Callable = lambda: ...,
):
    """work"""

    def inner(func):
        """inner"""

        functools.wraps(func)

        def decorator(*args, **kwargs):
            """decorator"""

            if "kwargs" in func.__code__.co_varnames:
                kwargs["__before__"] = before()

                if pass_work:
                    kwargs["__work__"] = "pass_work"

                if pass_works:
                    kwargs["__works__"] = "pass_works"

                if pass_context:
                    kwargs["__context__"] = "pass_context"

            func(*args, **kwargs)
            after()

        return decorator

    return inner


class AbstractWork(ABC):
    """Base work type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    @abstractmethod
    def handle(self, **kwargs):
        "Force implement function"

        raise NotImplementedError("handle not implemented.")


class DagExecutor:
    """DagExecutor"""

    def __init__(self) -> None:
        """DagExecutor constructor"""

        self._dag = DAG()

    @property
    @abstractproperty
    def vertices(self) -> list[Any]:
        """Get unit_of_works"""

    @final
    def setup_dag(self) -> bool:
        """Setup DAG"""

        self._dag.add_vertex(*self.vertices)

        for index in range(1, len(self.vertices)):
            self._dag.add_edge(self.vertices[index - 1], self.vertices[index])

    @final
    def execute_dag(self) -> list[Any]:
        """Execute the dag"""

        resp = dag_run(
            self._dag,
            processor=SequentialProcessor(),
            executor=LinearExecutor(),
        )

        return resp


class WorkGroup(DagExecutor):
    """Collection of Work"""

    def __init__(self, works: list[AbstractWork] | WorkList = None) -> None:
        """Constructor"""

        super().__init__()

        self._name = type(self).__name__

        if not isinstance(works, list) and not isinstance(works, WorkList):
            raise TypeError("Type mismatch for `works`.")

        self._works: WorkList = (
            works if isinstance(works, WorkList) else WorkList.from_works(works)
        )

        self.setup_dag()

    @property
    def vertices(self) -> WorkList:
        return self._works if self._works else WorkList()


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
    def __validate(wgs: list[WorkGroup]) -> bool:
        """Validate tasks are ok"""

        if not all([isinstance(wg, WorkGroup) for wg in wgs]):
            raise TypeError("Unsupported workgroup found.")

        return True


class LinearExecutor:
    """Linear executor"""

    def param(self, vertex: Any) -> Any:
        """Selecting parameters"""

        return vertex

    def execute(self, work_fn: AbstractWork | WorkGroup) -> Any:
        """Execute"""

        if isinstance(work_fn, WorkExecFrame):
            return work_fn.function()
        elif isinstance(work_fn, WorkGroup):
            return work_fn.execute_dag()
        else:
            raise TypeError(f"Incorrect type of `work` {type(work_fn)} found.")
