"""
Test module for WorkExecFrame
"""

from types import FunctionType

from hence import WorkExecFrame, AbstractWork


class TestWorkExecFrame:
    """TestWorkExecFrame"""

    @staticmethod
    def test__dont_set_id__when_id_not_passed():
        """test__dont_set_id__when_id_not_passed"""

        wef = WorkExecFrame()
        assert getattr(wef, "_id") == ""

    @staticmethod
    def test__get_id_set__when_id_passed():
        """test__get_id_set__when_id_passed"""

        wef = WorkExecFrame("WorkExecFrame")
        assert getattr(wef, "_id") == "WorkExecFrame"

    @staticmethod
    def test__dont_set_title__when_title_not_passed():
        """test__dont_set_title__when_title_not_passed"""

        wef = WorkExecFrame()
        assert getattr(wef, "_title") == ""

    @staticmethod
    def test__get_id_set__when_title_passed():
        """test__get_title_set__when_title_passed"""

        wef = WorkExecFrame("WorkExecFrame", "WorkExecFrame")
        assert getattr(wef, "_title") == "WorkExecFrame"

    @staticmethod
    def test__function_is_ellipsis__when_function_not_passed():
        """test__function_is_ellipsis__when_function_not_passed"""

        wef = WorkExecFrame()
        assert wef.function() == Ellipsis

    @staticmethod
    def test__function_is_not_ellipsis__when_function_passed():
        """test__function_is_not_ellipsis__when_function_passed"""

        def fn():
            """fn"""

            return "ABC"

        wef = WorkExecFrame("WorkExecFrame", "WorkExecFrame", function=fn)
        assert wef.function() == "ABC"

    @staticmethod
    def test__type_of_function__found_callable_function():
        """test__type_of_function__found_callable_function"""

        def fn():
            """fn"""

            return "ABC"

        wef = WorkExecFrame("WorkExecFrame", "WorkExecFrame", function=fn)
        assert getattr(wef, "_function_type") is FunctionType

    @staticmethod
    def test__type_of_function__found_callable_class():
        """test__type_of_function__found_callable_class"""

        class ClientWork(AbstractWork):
            """ClientWork"""

            def __work__(self, **kwargs):
                return "ClientWork"

        wef = WorkExecFrame("WorkExecFrame", "WorkExecFrame", function=ClientWork())
        assert getattr(wef, "_function_type") is AbstractWork

    @staticmethod
    def test__run_executes__when_no_params_given():
        """test__run_executes__when_no_params_given"""

        class ClientWork(AbstractWork):
            """ClientWork"""

            def __work__(self, **kwargs):
                return "ClientWork"

        wef = WorkExecFrame("WorkExecFrame", "WorkExecFrame", function=ClientWork())
        wef.run()

        assert wef.function_out == "ClientWork"

    @staticmethod
    def test__run_executes__when_params_given():
        """test__run_executes__when_params_given"""

        class ClientWork(AbstractWork):
            """ClientWork"""

            def __work__(self, **kwargs):
                return kwargs["param"]

        wef = WorkExecFrame("WorkExecFrame", "WorkExecFrame", function=ClientWork())
        wef.run(param="ClientWork")

        assert wef.function_out == "ClientWork"
