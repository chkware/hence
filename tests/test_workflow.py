"""
Hence tests Workflow
"""

from hence import Workflow, WorkGroup, AbstractWork, WorkExecFrame


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

            def __work__(self, **kwargs):
                print(type(self).__name__)

        wf = Workflow([WorkGroup([WorkExecFrame(function=ImplementedWork())])])

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

            def __work__(self, **kwargs):
                print(1)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __work__(self, **kwargs):
                print(2)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __work__(self, **kwargs):
                print(3)

        class ImplementedWork4(AbstractWork):
            """ImplementedWork4"""

            def __work__(self, **kwargs):
                print(4)

        wf = Workflow(
            [
                WorkGroup(
                    [
                        WorkExecFrame(function=ImplementedWork1()),
                        WorkExecFrame(function=ImplementedWork2()),
                    ]
                ),
                WorkGroup(
                    [
                        WorkExecFrame(function=ImplementedWork3()),
                        WorkExecFrame(function=ImplementedWork4()),
                    ]
                ),
            ]
        )

        wf.execute_dag()

        out, _ = capsys.readouterr()
        assert out == "1\n2\n3\n4\n"

    @staticmethod
    def test__wf_execute_pass__when_wg_do_not_share_session_data():
        """test__wf_execute_pass__when_wg_do_not_share_session_data"""

        class ImplementedWork1(AbstractWork):
            """ImplementedWork1"""

            def __work__(self, **kwargs):
                return f"1 __works__: {kwargs.get('__works__')}"

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __work__(self, **kwargs):
                return f"2 __works__: {kwargs.get('__works__')}"

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __work__(self, **kwargs):
                return f"3 __works__: {kwargs.get('__works__')}"

        class ImplementedWork4(AbstractWork):
            """ImplementedWork4"""

            def __work__(self, **kwargs):
                return f"4 __works__: {kwargs.get('__works__')}"

        wf = Workflow(
            [
                WorkGroup(
                    [
                        WorkExecFrame(id_="s1", function=ImplementedWork1()),
                        WorkExecFrame(id_="s2", function=ImplementedWork2()),
                    ]
                ),
                WorkGroup(
                    [
                        WorkExecFrame(id_="s3", function=ImplementedWork3()),
                        WorkExecFrame(id_="s4", function=ImplementedWork4()),
                    ]
                ),
            ]
        )

        resp = wf.execute_dag()
        resp_out = ""

        for _wg in resp:
            for _wl in _wg.vertices:
                if isinstance(_wl, WorkExecFrame):
                    resp_out += _wl.function_out

        assert (
            resp_out
            == """1 __works__: {}"""
            + """2 __works__: {'s1': '1 __works__: {}'}"""
            + """3 __works__: {}"""
            + """4 __works__: {'s3': '3 __works__: {}'}"""
        )
