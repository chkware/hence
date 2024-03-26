"""
Tests for work
"""

from typing import Any
import pytest

from hence import AbstractWork


class TestWork:
    """TestStep"""

    @staticmethod
    def test__create_work__fails_for_abstract_work():
        """test create_Step fails for AbstractWork"""

        with pytest.raises(TypeError):
            AbstractWork()

    @staticmethod
    def test__create_work__pass_for_child_step():
        """test create_Step pass for child Step"""

        class ChildWork(AbstractWork):
            """ChildWork"""

            def __work__(self, **kwargs) -> None:
                """ChildWork.handle"""

        ChildWork()

    @staticmethod
    def test__create_work__pass_when_executed(capsys):
        """test create_step pass when executed"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __work__(self, **kwargs):
                print(type(self).__name__)
                print(";".join([f"{key}={val}" for key, val in kwargs.items()]))

        iw = ImplementedWork()
        iw(row=1, column=2)

        out, _ = capsys.readouterr()

        assert out.strip() == "ImplementedWork\nrow=1;column=2;__before__=Ellipsis"
        assert iw._name == "ImplementedWork"

    @staticmethod
    def test__callable_returns_value__when_called(capsys):
        """test__ellipsis_returns__when_before_not_given"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __work__(self, **kwargs):
                return kwargs

        iw = ImplementedWork()
        return_var = iw(row=1)
        assert return_var.get("__before__") == Ellipsis


class TestWorkBeforeAndAfter:
    """test workgroup before and after"""

    @staticmethod
    def test__before_returns__when_before_given(capsys):
        """test__ellipsis_returns__when_before_not_given"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __before__(self) -> Any:
                return "from__before__"

            def __work__(self, **kwargs):
                print(repr(kwargs))

        iw = ImplementedWork()
        iw(row=1)

        out, _ = capsys.readouterr()
        assert out.strip() == """{'row': 1, '__before__': 'from__before__'}"""

    @staticmethod
    def test__ellipsis_returns__when_before_not_given(capsys):
        """test__ellipsis_returns__when_before_not_given"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __work__(self, **kwargs):
                print(repr(kwargs))

        iw = ImplementedWork()
        iw(row=1)

        out, _ = capsys.readouterr()
        assert out.strip() == """{'row': 1, '__before__': Ellipsis}"""

    @staticmethod
    def test__after_called__when_after_given(capsys):
        """test__after_called__when_after_given"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __before__(self) -> Any: ...

            def __work__(self, **kwargs):
                print(repr(kwargs))

            def __after__(self):
                print("__after__")

        iw = ImplementedWork()
        iw(row=1)

        out, _ = capsys.readouterr()
        assert out.strip() == """{'row': 1, '__before__': None}\n__after__"""
