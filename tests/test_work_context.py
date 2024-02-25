"""Work context test"""

from contextvars import ContextVar
from hence import ContextValues, get_context


def test__get_context__pass():
    """test__get_context__pass"""

    ctx = get_context()

    assert isinstance(ctx, ContextVar)
    assert isinstance(ctx.get(), ContextValues)
