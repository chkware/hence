"""
Hench tests
"""

import pytest

from hence import Workflow, WorkGroup, AbstractWork


class TestWorkflow:
    """TestWorkflow"""

    @staticmethod
    def test__create_workflow__pass_for_workflow():
        """test create_workflow pass for child workflow"""

        cw = Workflow()

        assert cw._name == "Workflow"


class TestWorkFlowExecute:
    """TestWorkFlowExecute"""

    @staticmethod
    def test__wf_execute_pass__when_wg_added(capsys):
        """test__wf_execute_pass__when_wg_added"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self):
                print(type(self).__name__)

        wf = Workflow([WorkGroup([ImplementedWork()])])

        wf.execute_dag()

        out, _ = capsys.readouterr()
        assert out.strip() == "ImplementedWork"

    @staticmethod
    def test__wf_execute_pass__when_wg_empty(capsys):
        """test__wf_execute_pass__when_wg_empty"""

        wf = Workflow([WorkGroup([])])

        wf.execute_dag()

        out, _ = capsys.readouterr()
        assert out.strip() == ""

    @staticmethod
    def test__wf_execute_pass__when_wf_empty(capsys):
        """test__wf_execute_pass__when_wf_empty"""

        wf = Workflow([])

        wf.execute_dag()

        out, _ = capsys.readouterr()
        assert out.strip() == ""

    @staticmethod
    def test__wf_execute_pass__when_wg_do_sequential_work(capsys):
        """test__wf_execute_pass__when_wg_do_sequential_work"""

        class ImplementedWork1(AbstractWork):
            """ImplementedWork1"""

            def __call__(self):
                print(1)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __call__(self):
                print(2)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __call__(self):
                print(3)

        class ImplementedWork4(AbstractWork):
            """ImplementedWork4"""

            def __call__(self):
                print(4)

        wf = Workflow(
            [
                WorkGroup(
                    [
                        ImplementedWork1(),
                        ImplementedWork2(),
                    ]
                ),
                WorkGroup(
                    [
                        ImplementedWork3(),
                        ImplementedWork4(),
                    ]
                ),
            ]
        )

        wf.execute_dag()

        out, _ = capsys.readouterr()
        assert out == "1\n2\n3\n4\n"


class TestWorkGroup:
    """TestTask"""

    @staticmethod
    def test__create_wg__pass_with_steps_set():
        """test create work group pass with steps set"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self):
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

            def __call__(self):
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

            def __call__(self):
                print(type(self).__name__)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __call__(self):
                print(type(self).__name__)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __call__(self):
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

            def __call__(self):
                print(type(self).__name__)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __call__(self):
                print(type(self).__name__)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __call__(self):
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

            def __call__(self) -> None:
                """ChildWork.__init__"""

        ChildWork()

    @staticmethod
    def test__create_work__pass_when_executed(capsys):
        """test create_step pass when executed"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self):
                print(type(self).__name__)

        iw = ImplementedWork()
        iw()

        out, _ = capsys.readouterr()

        assert out.strip() == "ImplementedWork"
        assert iw._name == "ImplementedWork"
