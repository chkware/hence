"""
Hench tests
"""

import pytest

from hence import AbstractWorkflow


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
