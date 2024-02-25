"""
Hench
"""

import abc
from collections import UserDict
from contextvars import ContextVar
import functools
from typing import Any, Callable, NamedTuple, final

from paradag import DAG, SequentialProcessor, dag_run


class WorkExecFrame(NamedTuple):
    """WorkFrame holds what goes inside works"""

    work_func: Callable = lambda: ...
    work_exec_output: Any = None


class ContextValues(UserDict):
    """ContextValues"""


context: ContextVar[ContextValues] = ContextVar(
    "context", default=ContextValues({"works": []})
)


def get_context(ctx=context):
    """get context"""

    return ctx


def get_works(ctx=context):
    """get_works"""

    if "works" in ctx:
        return ctx["works"]

    raise RuntimeError("Misconfigured context.")


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

            kwargs["__before__"] = before()

            if pass_work:
                kwargs["__work__"] = "pass_work"

            if pass_works:
                kwargs["__works__"] = "pass_works"

            if pass_context:
                kwargs["__context__"] = "pass_context"

            print(title, pass_work, pass_works, args, kwargs)
            func(*args, **kwargs)
            after()

        return decorator

    return inner


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

        if isinstance(work_fn, AbstractWork) and callable(work_fn):
            return work_fn()
        elif isinstance(work_fn, WorkGroup):
            return work_fn.execute_dag()
        else:
            raise TypeError(f"Incorrect type of `work` {type(work_fn)} found.")
