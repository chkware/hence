"""
Hench tests Workflow
"""

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

            def __call__(self, **kwargs):
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

            def __call__(self, **kwargs):
                print(1)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __call__(self, **kwargs):
                print(2)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __call__(self, **kwargs):
                print(3)

        class ImplementedWork4(AbstractWork):
            """ImplementedWork4"""

            def __call__(self, **kwargs):
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


# def pass_context(): ...
# def pass_previous_step(): ...
# def pass_steps(): ...
# def work(id, before, after): ...


# @pass_context
# @pass_previous_step
# @pass_steps
# @work(id, before=..., after=...)
# def step_function(steps, previous_step, context): ...
