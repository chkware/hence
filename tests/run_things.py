"""..."""

import functools
from typing import Callable


def work(
    title,
    pass_step: bool = False,
    pass_steps: bool = False,
    pass_context: bool = False,
    pass_before_ret: bool = False,
    before: Callable = lambda: ...,
    after: Callable = lambda: ...,
):
    """work"""

    def inner(func):
        """inner"""

        functools.wraps(func)

        def decorator(*args, **kwargs):
            # def decorator():
            """decorator"""

            print("title:", title)
            print("pass_step:", pass_step)
            print("pass_steps:", pass_steps)
            print("args:", args)
            print("kwargs:", kwargs)

            args_local = []
            args_temp = args
            kwargs_temp = kwargs
            t_func = func
            t_before_resp = before()

            # print("t_before_resp type:", type(t_before_resp))
            # print(t_before_resp == Ellipsis)

            for param in func.__code__.co_varnames:
                if param == "step" and pass_step:
                    args_local.append("step")
                elif param == "steps" and pass_steps:
                    args_local.append("steps")
                elif param == "context" and pass_context:
                    args_local.append("context")
                elif param == "before" and pass_before_ret:
                    args_local.append(t_before_resp)
                elif param == "args":
                    t_func = functools.partial(func, args=args)
                elif param == "kwargs":
                    t_func = functools.partial(func, **kwargs)
                else:
                    if len(kwargs_temp) > 0 and param in kwargs_temp:
                        args_local.append(kwargs_temp[param])
                        del kwargs_temp[param]
                    elif len(args_temp) > 0:
                        args_local.append(args_temp[0])
                        args_temp = args_temp[1:]

            print("func.__code__.co_varnames:", func.__code__.co_varnames)
            print("args_local", args_local)
            args_local_tpl = tuple(args_local)

            t_func(*args_local_tpl)
            after()

        return decorator

    return inner


@work("run", pass_step=True, pass_steps=True, pass_context=True, pass_before_ret=True)
def something(step, before, a, b, s: str, *args, **kwargs):
    """something"""

    print(s or "something", step, before, args, kwargs, a, b)


# something()
# print("---------")
# print()
something(2, 3, s="Hasan", aim=1, bin=45)
