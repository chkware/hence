"""
Hench tests
"""

import pytest

from hence import AbstractWorkflow, AbstractTask, AbstractStep


class TestWorkflow:
    """TestWorkflow"""

    @staticmethod
    def test__create_workflow__fails_for_abstractworkflow():
        """test create_workflow fails for AbstractWorkflow"""

        with pytest.raises(TypeError):
            AbstractWorkflow()

    @staticmethod
    def test__create_workflow__pass_for_child_workflow():
        """test create_workflow pass for child workflow"""

        class ChildWorkflow(AbstractWorkflow):
            """ChildWorkflow"""

            def execute(self) -> None:
                """ChildWorkflow.__init__"""

                super().execute()

        cw = ChildWorkflow()

        assert cw._name == "ChildWorkflow"


class TestTask:
    """TestTask"""

    @staticmethod
    def test__create_task__fails_for_abstracttask():
        """test create_Task fails for AbstractTask"""

        with pytest.raises(TypeError):
            AbstractTask()

    @staticmethod
    def test__create_task__pass_for_child_task():
        """test create_Task pass for child Task"""

        class ChildTask(AbstractTask):
            """ChildTask"""

            def execute(self) -> None:
                """ChildTask.__init__"""

                super().execute()

        ChildTask()

    @staticmethod
    def test__create_task__pass_with_steps_set():
        """test create_task pass with steps set"""

        class ChildTask(AbstractTask):
            """ChildTask"""

            def execute(self) -> None:
                """ChildTask.__init__"""

                super().execute()

        class ImplementedStep(AbstractStep):
            def __call__(self):
                print("ImplementedStep.__call__")

        ct = ChildTask(
            [
                ImplementedStep(),
                ImplementedStep(),
            ]
        )

        assert isinstance(ct, ChildTask)
        assert ct._name == "ChildTask"

    @staticmethod
    def test__create_task__fail_when_wrong_step_set():
        """test create_task fail when wrong step set"""

        class ChildTask(AbstractTask):
            """ChildTask"""

            def execute(self) -> None:
                """ChildTask.__init__"""

                super().execute()

        class ImplementedStep(AbstractStep):
            def __call__(self):
                print("ImplementedStep.__call__")

        with pytest.raises(TypeError):
            ChildTask(
                [
                    ImplementedStep(),
                    map,
                ]
            )

    @staticmethod
    def test__create_task__pass_for_dag_creation():
        """test create_task pass for dag creation"""

        class ChildTask(AbstractTask):
            """ChildTask"""

            def execute(self) -> None:
                """ChildTask.__init__"""

                super().execute()

        class ImplementedStep1(AbstractStep):
            def __call__(self):
                print("ImplementedStep1.__call__")

        class ImplementedStep2(AbstractStep):
            def __call__(self):
                print("ImplementedStep2.__call__")

        class ImplementedStep3(AbstractStep):
            def __call__(self):
                print("ImplementedStep3.__call__")

        ct = ChildTask(
            [
                ImplementedStep1(),
                ImplementedStep2(),
                ImplementedStep3(),
            ]
        )

        assert ct._dag.vertex_size() == 3
        assert ct._dag.edge_size() == 2


class TestStep:
    """TestStep"""

    @staticmethod
    def test__create_step__fails_for_abstractstep():
        """test create_Step fails for AbstractStep"""

        with pytest.raises(TypeError):
            AbstractStep()

    @staticmethod
    def test__create_step__pass_for_child_step():
        """test create_Step pass for child Step"""

        class ChildStep(AbstractStep):
            """ChildStep"""

            def __call__(self) -> None:
                """ChildStep.__init__"""

        ChildStep()

    @staticmethod
    def test__create_step__pass_when_executed(capsys):
        """test create_step pass when executed"""

        class ImplementedStep(AbstractStep):
            def __call__(self):
                print("ImplementedStep.__call__")

        iss = ImplementedStep()
        iss()

        out, _ = capsys.readouterr()

        assert out.strip() == "ImplementedStep.__call__"
        assert iss._name == "ImplementedStep"
