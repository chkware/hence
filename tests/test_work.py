"""
Tests for work
"""

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

            def __call__(self, **kwargs) -> None:
                """ChildWork.handle"""

        ChildWork()

    @staticmethod
    def test__create_work__pass_when_executed(capsys):
        """test create_step pass when executed"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self, **kwargs):
                print(type(self).__name__)
                print(";".join([f"{key}={val}" for key, val in kwargs.items()]))

        iw = ImplementedWork()
        iw(row=1, column=2)

        out, _ = capsys.readouterr()

        assert out.strip() == "ImplementedWork\nrow=1;column=2"
        assert iw._name == "ImplementedWork"
