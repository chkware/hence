"""
# A very minimal web scraping examples using class
#
# ----------------------------------------
# Following code example SHOULD NOT be used
# in production scenario
# ----------------------------------------
"""

import csv
from urllib import request

from hence import AbstractWork, WorkGroup, WorkList, WorkExecFrame


class FetchContent(AbstractWork):
    """FetchContent"""

    def __work__(self, **kwargs) -> str:
        """Fetch the content of example.org"""

        with request.urlopen("https://example.org/") as response:
            return response.read().hex()


class GetTheTitle(AbstractWork):
    """GetTheTitle"""

    def __work__(self, **kwargs) -> dict:
        """Parse the content in <title>"""

        html = kwargs.get("__works__")["fetch_content"]
        html = bytes.fromhex(html).decode("utf-8")

        html.find("<h1>")
        title = html[html.find("<h1>") + len("<h1>") : html.find("</h1>")]
        body = html[html.find("<p>") + len("<p>") : html.find("</p>")]

        return dict(title=title, body=body)


class SaveToCsv(AbstractWork):
    """SaveToCsv"""

    def __work__(self, **kwargs) -> str:
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
                WorkExecFrame(id_="fetch_content", function=FetchContent()),
                WorkExecFrame(id_="get_the_title", function=GetTheTitle()),
                WorkExecFrame(id_="save_to_csv", function=SaveToCsv()),
            ]
        )
    )

    grp.execute_dag()
