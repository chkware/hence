"""Work context test"""

from contextvars import ContextVar
import inspect

import pytest

from hence import WorkList, WorkExecFrame, work


@pytest.fixture
def make_context():
    """make and return a context"""
    return ContextVar("context", default=WorkList())


class TestWorkDecorator:
    """TestWorkDecorator"""

    @staticmethod
    def test__works_dec__pass_for_no_arg(capsys):
        """test__set_works__pass"""

        @work()
        def task_one(**kwargs):
            print(inspect.currentframe().f_code.co_name)

        task_one()
        out, _ = capsys.readouterr()
        assert out.strip() == "task_one"

    @staticmethod
    def test__works_dec__pass_for_passed_params(capsys):
        """test__set_works__pass"""

        @work()
        def task_one(ae, af, **kwargs):
            print(ae, af)

        task_one(ae=1, af=2)
        out, _ = capsys.readouterr()
        assert out.strip() == "1 2"

    @staticmethod
    def test__works_dec__pass_for_passed_named_params_cap_before(capsys):
        """test__set_works__pass"""

        @work()
        def task_one(ae, af, **kwargs):
            print(ae, af, kwargs)

        task_one(ae=1, af=2)
        out, _ = capsys.readouterr()
        assert out.strip() == "1 2 {'__before__': Ellipsis}"

    @staticmethod
    def test__works_dec__pass_for_passed_named_params_cap_vars(capsys):
        """test__set_works__pass"""

        def before_():
            return "before_"

        @work(before=before_)
        def task_one(ae, af, **kwargs):
            print(ae, af, kwargs)

        task_one(ae=1, af=2, a=1)
        out, _ = capsys.readouterr()
        assert out.strip() == "1 2 {'a': 1, '__before__': 'before_'}"

    @staticmethod
    def test__works_dec__pass_for_passed_named_params_cap_vars_args(capsys):
        """test__set_works__pass"""

        def before_():
            return "before_"

        @work(before=before_)
        def task_one(ae, af, a=2, **kwargs):
            print(ae, af, a, kwargs)

        task_one(ae=1, af=2, g=[3, 4, 5], a=1)
        out, _ = capsys.readouterr()
        assert out.strip() == "1 2 1 {'g': [3, 4, 5], '__before__': 'before_'}"


# setup @work


# def test__work_set__pass():
#     """test__work_set__pass"""

#     def before_():
#         return "before_"

#     @work("task one", before=before_)
#     def task_one(*args, **kwargs):
#         print(args, kwargs)

#     task_one(1, 2, 3, 4, 5, a=1, bun="js")

#     #
#     ctx_val = get_context().get()
#     print(ctx_val)

#     # ctx_val["works"]
