"""Work context test"""

from contextvars import ContextVar

# import inspect

from hence import ContextHandler, ContextValues


class TestContextHandlerSanity:
    """TestContextHandlerSanity"""

    @staticmethod
    def test_create_pass_for_empty_object():
        """test create passes"""

        ctx_handler = ContextHandler()

        assert isinstance(ctx_handler._context, ContextVar)
        assert ctx_handler._token is None

    @staticmethod
    def test_create_pass_for_same_session():
        """test_create_pass_for_same_session"""

        ctx_handler_1 = ContextHandler()
        ctx_handler_2 = ContextHandler()

        assert ctx_handler_1._token is ctx_handler_2._token
        assert ctx_handler_1 is not ctx_handler_2

    @staticmethod
    def test_create_pass_for_setting_and_getting_from_same_ctx():
        """
        test create pass for setting and getting from same context session
        """

        ctx_handler_1 = ContextHandler()
        ctx = ctx_handler_1.get_context()

        a = ContextValues({"works": []})
        ctx.set()

        ctx_handler_2 = ContextHandler()


class TestContextHandlerGetContext:
    """TestContextHandlerGetContext"""

    @staticmethod
    def test__get_context__pass():
        """test__get_context__pass"""

        chx = ContextHandler()

        ctx = chx.get_context()
        ctxvar = ctx.get()

        assert isinstance(ctx, ContextVar)
        assert isinstance(ctxvar, ContextValues)
        assert "works" in ctxvar


# from contextvars import ContextVar
# import inspect

# from hence import ContextValues, get_context, work


# def test__get_context__pass():
#     """test__get_context__pass"""

#     ctx = get_context()
#     ctxvar = ctx.get()

#     assert isinstance(ctx, ContextVar)
#     assert isinstance(ctxvar, ContextValues)
#     assert "works" in ctxvar


# def test__works_dec__pass_for_no_arg(capsys):
#     """test__set_works__pass"""

#     @work("task one")
#     def task_one():
#         print(inspect.currentframe().f_code.co_name)

#     task_one()
#     out, _ = capsys.readouterr()
#     assert out.strip() == "task_one"


# def test__works_dec__pass_for_passed_params(capsys):
#     """test__set_works__pass"""

#     @work("task one")
#     def task_one(ae, af):
#         print(ae, af)

#     task_one(1, 2)
#     out, _ = capsys.readouterr()
#     assert out.strip() == "1 2"


# def test__works_dec__pass_for_passed_named_params_cap_before(capsys):
#     """test__set_works__pass"""

#     @work("task one")
#     def task_one(ae, af, **kwargs):
#         print(ae, af, kwargs)

#     task_one(1, 2)
#     out, _ = capsys.readouterr()
#     assert out.strip() == "1 2 {'__before__': Ellipsis}"


# def test__works_dec__pass_for_passed_named_params_cap_vars(capsys):
#     """test__set_works__pass"""

#     def before_():
#         return "before_"

#     @work("task one", before=before_)
#     def task_one(ae, af, **kwargs):
#         print(ae, af, kwargs)

#     task_one(1, 2, a=1)
#     out, _ = capsys.readouterr()
#     assert out.strip() == "1 2 {'a': 1, '__before__': 'before_'}"


# def test__works_dec__pass_for_passed_named_params_cap_vars_args(capsys):
#     """test__set_works__pass"""

#     def before_():
#         return "before_"

#     @work("task one", before=before_)
#     def task_one(ae, af, *args, a=2, **kwargs):
#         print(ae, af, args, a, kwargs)

#     task_one(1, 2, 3, 4, 5, a=1)
#     out, _ = capsys.readouterr()
#     assert out.strip() == "1 2 (3, 4, 5) 1 {'__before__': 'before_'}"


# def test__works_dec__pass_for_passed_params_cap_vars_args(capsys):
#     """test__set_works__pass"""

#     def before_():
#         return "before_"

#     @work("task one", before=before_)
#     def task_one(*args, **kwargs):
#         print(args, kwargs)

#     task_one(1, 2, 3, 4, 5, a=1, bun="js")
#     out, _ = capsys.readouterr()
#     assert (
#         out.strip() == "(1, 2, 3, 4, 5) {'a': 1, 'bun': 'js', '__before__': 'before_'}"
#     )


# setup @work


# def test__work_set__pass():
#     """test__work_set__pass"""

#     def before_():
#         return "before_"

#     @work("task one", before=before_)
#     def task_one(*args, **kwargs):
#         print(args, kwargs)

#     task_one(1, 2, 3, 4, 5, a=1, bun="js")

#     #
#     ctx_val = get_context().get()
#     print(ctx_val)

#     # ctx_val["works"]
