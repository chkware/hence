"""..."""

import functools
from typing import Callable


def work(
    title,
    pass_step: bool = False,
    pass_steps: bool = False,
    pass_context: bool = False,
    before: Callable = lambda: ...,
    after: Callable = lambda: ...,
):
    """work"""

    def inner(func):
        """inner"""

        functools.wraps(func)

        def decorator(*args, **kwargs):
            """decorator"""

            kwargs["__before__"] = before()

            if pass_step:
                kwargs["__step__"] = "passed_step"

            if pass_steps:
                kwargs["__steps__"] = "passed_steps"

            if pass_context:
                kwargs["__context__"] = "pass_context"

            print(title, pass_step, pass_steps, args, kwargs)
            func(*args, **kwargs)
            after()

        return decorator

    return inner


@work("run", pass_step=True, pass_steps=True, pass_context=True)
def something(s: str = None, *args, **kwargs):
    """something"""

    print(s or "something", args, kwargs)


something()
print("---------")
something("Hasan")
