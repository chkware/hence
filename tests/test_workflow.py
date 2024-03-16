"""
Hench tests Workflow
"""

from hence import WorkList, Workflow, WorkGroup, AbstractWork, WorkExecFrame


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

        wf = Workflow(
            [WorkGroup(WorkList([WorkExecFrame(function=ImplementedWork())]))]
        )

        wf.execute_dag()

        out, _ = capsys.readouterr()
        assert out.strip() == "ImplementedWork"

    @staticmethod
    def test__wf_execute_pass__when_wg_empty(capsys):
        """test__wf_execute_pass__when_wg_empty"""

        wf = Workflow([WorkGroup(WorkList())])

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

        wl1 = WorkList()
        wl1.append(WorkExecFrame(function=ImplementedWork1()))
        wl1.append(WorkExecFrame(function=ImplementedWork2()))

        wl2 = WorkList()
        wl2.append(WorkExecFrame(function=ImplementedWork3()))
        wl2.append(WorkExecFrame(function=ImplementedWork4()))

        wf = Workflow(
            [
                WorkGroup(wl1),
                WorkGroup(wl2),
            ]
        )

        wf.execute_dag()

        out, _ = capsys.readouterr()
        assert out == "1\n2\n3\n4\n"
