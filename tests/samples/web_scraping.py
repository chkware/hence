"""
# A very minimal web scraping examples
#
# ----------------------------------------
# Following code example SHOULD NOT be used
# in production scenario
# ----------------------------------------
"""

import csv
from urllib import request

from hence import work, WorkGroup, WorkList, WorkExecFrame


@work()
def fetch_content(**kwargs) -> str:
    """Fetch the content of example.org"""

    with request.urlopen("https://example.org/") as response:
        return response.read().hex()


@work()
def get_the_title(**kwargs) -> dict:
    """Parse the content in <title>"""

    html = kwargs.get("__works__")["fetch_content"]
    html = bytes.fromhex(html).decode("utf-8")

    html.find("<h1>")
    title = html[html.find("<h1>") + len("<h1>") : html.find("</h1>")]
    body = html[html.find("<p>") + len("<p>") : html.find("</p>")]

    return dict(title=title, body=body)


@work()
def save_to_csv(**kwargs) -> str:
    """save the content to csv"""

    ret = kwargs.get("__works__")["get_the_title"]

    with open("example.org-data.csv", "w+", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["title", "description"])
        writer.writerow([ret["title"], ret["body"]])


def test_main():
    """main"""

    grp = WorkGroup(
        WorkList(
            [
                WorkExecFrame(id_="fetch_content", function=fetch_content),
                WorkExecFrame(id_="get_the_title", function=get_the_title),
                WorkExecFrame(id_="save_to_csv", function=save_to_csv),
            ]
        )
    )

    grp.execute_dag()
