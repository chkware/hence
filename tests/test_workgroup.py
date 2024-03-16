"""
Tests for workgroup
"""

import pytest

from hence import AbstractWork, WorkGroup, WorkList, WorkExecFrame


class TestWorkGroup:
    """TestTask"""

    @staticmethod
    def test__create_wg__pass_with_steps_set():
        """test create work group pass with steps set"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        wg = WorkGroup(
            WorkList.from_works(
                [
                    ImplementedWork(),
                    ImplementedWork(),
                ]
            )
        )

        assert isinstance(wg, WorkGroup)
        assert wg._name == "WorkGroup"

    @staticmethod
    def test__create_wg__fail_when_wrong_step_set():
        """test create work group fail when wrong step set"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        with pytest.raises(TypeError):
            WorkGroup(
                [
                    ImplementedWork(),
                    map,
                ]
            )

    @staticmethod
    def test__create_wg__pass_with_work_list_params(capsys):
        """test create work group fail when wrong step set"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self, **kwargs):
                print(type(self).__name__)
                print(";".join([f"{key}={val}" for key, val in kwargs.items()]))

        wg = WorkGroup(
            WorkList(
                [
                    WorkExecFrame(
                        "ImplementedWork",
                        ImplementedWork(),
                        {"param1": 1, "param2": "ab"},
                    ),
                    WorkExecFrame(
                        "ImplementedWork",
                        ImplementedWork(),
                        {"param1": 2, "param2": "bc"},
                    ),
                ]
            )
        )

        wg.execute_dag()

        out, _ = capsys.readouterr()

        assert (
            out
            == "ImplementedWork\nparam1=1;param2=ab\nImplementedWork\nparam1=2;param2=bc\n"
        )

    @staticmethod
    def test__create_wg__pass_for_dag_creation():
        """test create work group pass for dag creation"""

        class ImplementedWork1(AbstractWork):
            """ImplementedWork1"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        wg = WorkGroup(
            WorkList.from_works(
                [
                    ImplementedWork1(),
                    ImplementedWork2(),
                    ImplementedWork3(),
                ]
            )
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

            def __call__(self, **kwargs):
                print(type(self).__name__)

        class ImplementedWork2(AbstractWork):
            """ImplementedWork2"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        class ImplementedWork3(AbstractWork):
            """ImplementedWork3"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        wg = WorkGroup(
            WorkList.from_works(
                [
                    ImplementedWork1(),
                    ImplementedWork2(),
                    ImplementedWork3(),
                ]
            )
        )

        resp = wg.execute_dag()
        out, _ = capsys.readouterr()

        assert out == "ImplementedWork1\nImplementedWork2\nImplementedWork3\n"
        assert len(resp) == 3


class TestWorkList:
    """TestWorkList"""

    @staticmethod
    def test__from_works__pass():
        """test__from_works__pass"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self, **kwargs):
                print(type(self).__name__)

        wl = WorkList.from_works(
            [
                ImplementedWork(),
                ImplementedWork(),
                ImplementedWork(),
            ]
        )

        assert isinstance(wl, WorkList)
        assert all(isinstance(item, WorkExecFrame) for item in wl)

    @staticmethod
    def test__from_works__fail_for_missing_kwargs():
        """test__from_works__fail_for_missing_kwargs"""

        class ImplementedWork(AbstractWork):
            """ImplementedWork"""

            def __call__(self):
                print(type(self).__name__)

        with pytest.raises(TypeError):
            WorkList.from_works(
                [
                    ImplementedWork(),
                ]
            )

    @staticmethod
    def test__from_works__fails_for_callable():
        """test__from_works__fails_for_callable"""

        with pytest.raises(TypeError):
            WorkList(
                [
                    map,
                    map,
                    map,
                ]
            )

    @staticmethod
    def test__set_item__fails_for_callable():
        """test__from_works__fails_for_callable"""

        with pytest.raises(TypeError):
            wl = WorkList()
            wl[1] = map
