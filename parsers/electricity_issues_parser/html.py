from typing import List

from bs4 import BeautifulSoup

from domain import ElectricityIssue
from repositories.electricity_issues_html_repository.base import (
    ElectricityIssuesHTMLRepositoryABC,
)

from .base import ElectricityIssuesParserABC


class ElectricityIssuesParserHTML(ElectricityIssuesParserABC):
    _electricity_issues_html_repository: ElectricityIssuesHTMLRepositoryABC

    def __init__(self, repo: ElectricityIssuesHTMLRepositoryABC):
        self._electricity_issues_html_repository = repo

    async def parse(self) -> List[ElectricityIssue]:
        html = await self._electricity_issues_html_repository.get_html_content()
        bs = BeautifulSoup(html, "html.parser")
        rows = bs.select("tr")
        result: List[ElectricityIssue] = []

        for row in rows:
            cols = row.select("td")
            skip = self._skip_row(cols)

            if skip or len(cols) != 9:
                continue

            result.append(
                ElectricityIssue(
                    start_off_date_text=cols[3].text,
                    start_off_time_text=cols[4].text,
                    start_on_date_text=cols[5].text,
                    start_on_time_text=cols[6].text,
                    place=cols[2].text,
                )
            )

        return result

    @staticmethod
    def _skip_row(cols: List[BeautifulSoup]) -> bool:
        for col in cols:
            if len(col.text.strip()) == 0:
                return True

        return False
