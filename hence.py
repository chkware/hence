"""
Hence
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections import UserList
from functools import wraps
from json import loads, dumps
from types import FunctionType
from typing import Any, Callable, Optional, final

from paradag import DAG, SequentialProcessor, dag_run


class WorkExecFrame:
    """WorkFrame holds what goes inside works"""

    OUT_KEY = "_result"

    def __init__(
        self,
        id_: str = "",
        title: str = "",
        function: Callable = lambda: ...,
        function_params: Optional[dict] = None,
    ) -> None:
        """Create WorkExecFrame"""

        if not isinstance(id_, str):
            raise TypeError("String value expected for id_.")

        self._id = id_

        if not isinstance(title, str):
            raise TypeError("String value expected for title.")

        self._title: str = title

        if not isinstance(function, Callable):
            raise TypeError("Function must be a callable.")

        self._function: Callable = function

        if isinstance(self._function, AbstractWork):
            self._function_type = AbstractWork
        else:
            self._function_type = FunctionType

        self.function_params = function_params if function_params else {}
        self.function_out = ""

    @property
    def id(self) -> str:
        """get the id"""

        return self._id

    @property
    def function(self) -> Callable:
        """get the function"""

        return self._function

    @property
    def function_params(self) -> dict:
        """get the function"""

        return loads(self._function_params)

    @function_params.setter
    def function_params(self, val: dict) -> None:
        """get the function"""

        if not isinstance(val, dict):
            raise TypeError("Function params must be a dict.")

        self._function_params = dumps(val)

    @property
    def function_out(self) -> dict:
        """get the function output"""

        return loads(self._function_out).get(self.OUT_KEY, {})

    @function_out.setter
    def function_out(self, val: Any) -> None:
        """function_out setter"""

        self._function_out = dumps({self.OUT_KEY: val})

    def run(self, **kwargs):
        """run the function and save the result to output"""

        if len(kwargs) > 0 and not isinstance(kwargs, dict):
            raise TypeError("Function params must be a dict.")

        params = self.function_params | kwargs
        self.function_out = self.function(**params)

        return self.function_out


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
        """Validate values before setting"""

        if not isinstance(value, (WorkExecFrame)):
            raise TypeError(f"WorkExecFrame expected, got {type(value).__name__}.")

        if not isinstance(value.function, (AbstractWork, FunctionType)):
            raise TypeError(
                f"Function of type AbstractWork or FunctionType expected, got {type(value).__name__}."
            )

        if (
            isinstance(value.function, AbstractWork)
            and "kwargs" not in value.function.__work__.__code__.co_varnames
        ):
            raise TypeError(
                f"Missing {type(value.function).__name__}.__work__(..., **kwargs)."
            )

        if (
            isinstance(value.function, FunctionType)
            and value.function.__code__.co_name != "decorator"
        ):
            raise TypeError("Unsupported work found. @work() decorated expected.")

        return value


def work(
    before: Callable = lambda: ...,
    after: Callable = lambda: ...,
):
    """work"""

    def inner(func):
        """inner"""

        if "kwargs" not in func.__code__.co_varnames:
            raise TypeError(f"Missing {type(func).__name__}(..., **kwargs).")

        @wraps(func)
        def decorator(**kwargs):
            """decorator"""

            kwargs["__before__"] = before()
            returnable = func(**kwargs)
            after()

            return returnable

        return decorator

    return inner


class AbstractWork(ABC):
    """Base work type"""

    def __init__(self) -> None:
        """Constructor"""

        self._name = type(self).__name__

    def __before__(self) -> Any:
        """default before impl"""

        return Ellipsis

    def __after__(self) -> Any:
        """default after impl"""

        return Ellipsis

    @abstractmethod
    def __work__(self, **kwargs):
        "Force implement function"

        raise NotImplementedError("__work__ not implemented.")

    def __call__(self, **kwargs):
        kwargs["__before__"] = self.__before__()
        returnable = self.__work__(**kwargs)
        self.__after__()

        return returnable


class DagExecutor:
    """DagExecutor"""

    def __init__(self) -> None:
        """DagExecutor constructor"""

        self._dag = DAG()

    @property
    @abstractmethod
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

    def __init__(self, works: WorkList) -> None:
        """Constructor"""

        super().__init__()

        self._name = type(self).__name__

        if not isinstance(works, WorkList):
            raise TypeError("Type mismatch for `works`. WorkList expected.")

        self._works: WorkList = works

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

    RES_KEY = "__works__"

    def __init__(self) -> None:
        """init LinearExecutor"""

        self._results = {}

    def param(self, vertex: Any) -> Any:
        """Selecting parameters"""

        return vertex

    def execute(self, __work: WorkExecFrame | WorkGroup) -> Any:
        """Execute"""

        if isinstance(__work, WorkExecFrame) and callable(__work.function):
            return __work.run(**{self.RES_KEY: self._results})
        elif isinstance(__work, WorkGroup):
            return __work.execute_dag()
        else:
            raise TypeError(f"Incorrect type of `work` {type(__work)} found.")

    def report_finish(self, vertices_result):
        """After execution finished"""

        for vertex, result in vertices_result:
            if not isinstance(vertex, WorkGroup) and len(vertex.id) > 0:
                self._results[vertex.id] = result
