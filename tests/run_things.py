"""..."""

from hence import work


@work("run", pass_work=True, pass_works=True, pass_context=True)
def something(s: str = None, *args, **kwargs):
    """something"""

    print(s or "something", args, kwargs)


something()
print("---------")
something("Hasan", 23, "some some", aida="ty")
