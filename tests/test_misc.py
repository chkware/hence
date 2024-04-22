"""Test Misc. func"""

import pytest
from hence import get_step_out


class TestGetStepOut:
    """Test cases for get_step_out()"""

    @staticmethod
    def test_fails_on_none_args():
        """Fails for none args"""

        args: dict = None

        with pytest.raises(TypeError):
            get_step_out(args, "some")

    @staticmethod
    def test_fails_on_empty_args():
        """Fails for empty args"""

        args = {}

        with pytest.raises(TypeError):
            get_step_out(args, "some")

    @staticmethod
    def test_fails_on_none_step_name():
        """Fails for none step_name"""

        args = {
            "step1": 1,
        }

        step_name: str = None

        with pytest.raises(TypeError):
            get_step_out(args, step_name)

    @staticmethod
    def test_fails_on_empty_step_name():
        """Fails for empty step_name"""

        args = {
            "step1": 1,
        }

        step_name: str = ""

        with pytest.raises(TypeError):
            get_step_out(args, step_name)

    @staticmethod
    def test_fails_when_works_not_found_in_args():
        """Fails for __works__ not found in args"""

        args = {
            "step1": 1,
        }

        step_name: str = "step1"

        with pytest.raises(TypeError):
            get_step_out(args, step_name)

    @staticmethod
    def test_fails_when_works_do_not_have_key():
        """Fails for not found step in args[__works__]"""

        args = {
            "__works__": {
                "step1": 1,
            }
        }

        step_name: str = "step2"

        with pytest.raises(TypeError):
            get_step_out(args, step_name)

    @staticmethod
    def test_pass_when_step_found():
        """Pass for found step in args[__works__]"""

        args = {
            "__works__": {
                "step1": 1,
            }
        }

        step_name: str = "step1"

        assert 1 == get_step_out(args, step_name)
