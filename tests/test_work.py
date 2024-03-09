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

            def handle(self) -> None:
                """ChildWork.__init__"""

        ChildWork()

    @staticmethod
    def test__create_work__pass_when_executed(capsys):
        """test create_step pass when executed"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def handle(self):
                print(type(self).__name__)

        iw = ImplementedWork()
        iw.handle()

        out, _ = capsys.readouterr()

        assert out.strip() == "ImplementedWork"
        assert iw._name == "ImplementedWork"
