"""..."""

from hence import work, WorkGroup, WorkList, WorkExecFrame


def test__a_thing():
    def other():
        return "Name"

    @work(before=other)
    def something(s: str = None, **kwargs):
        """something"""

        print(s or "something", kwargs)

    work_grp = WorkGroup(
        WorkList([WorkExecFrame(function=something, function_params={"s": "Hasan"})])
    )

    work_grp.execute_dag()
