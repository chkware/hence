"""
Hench tests
"""

import pytest

from hence import AbstractWorkflow, AbstractTask


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

        ChildWorkflow()


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
