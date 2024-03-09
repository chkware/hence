"""
Tests for workgroup
"""

import pytest

from hence import WorkGroup, AbstractWork


class TestWorkGroup:
    """TestTask"""

    @staticmethod
    def test__create_wg__pass_with_steps_set():
        """test create work group pass with steps set"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def handle(self):
                print(type(self).__name__)

        wg = WorkGroup(
            [
                ImplementedWork(),
                ImplementedWork(),
            ]
        )

        assert isinstance(wg, WorkGroup)
        assert wg._name == "WorkGroup"

    @staticmethod
    def test__create_wg__fail_when_wrong_step_set():
        """test create work group fail when wrong step set"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def handle(self):
                print(type(self).__name__)

        with pytest.raises(TypeError):
            WorkGroup(
                [
                    ImplementedWork(),
                    map,
                ]
            )

    @staticmethod
    def test__create_wg__pass_for_dag_creation():
        """test create work group pass for dag creation"""

        class ImplementedWork1(AbstractWork):
            """ImplementedWork1"""

            def handle(self):
                print(type(self).__name__)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def handle(self):
                print(type(self).__name__)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def handle(self):
                print(type(self).__name__)

        wg = WorkGroup(
            [
                ImplementedWork1(),
                ImplementedWork2(),
                ImplementedWork3(),
            ]
        )

        assert wg._dag.vertex_size() == 3
        assert wg._dag.edge_size() == 2


class TestWorkGroupExecute:
    """TestWorkGroupExecute"""

    @staticmethod
    def test__execute_wg__pass_when_steps_are_right(capsys):
        """test create_task pass for dag creation"""

        class ImplementedWork1(AbstractWork):
            """ImplementedWork1"""

            def handle(self):
                print(type(self).__name__)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def handle(self):
                print(type(self).__name__)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def handle(self):
                print(type(self).__name__)

        wg = WorkGroup(
            [
                ImplementedWork1(),
                ImplementedWork2(),
                ImplementedWork3(),
            ]
        )

        resp = wg.execute_dag()
        out, _ = capsys.readouterr()

        assert out == "ImplementedWork1\nImplementedWork2\nImplementedWork3\n"
        assert len(resp) == 3
