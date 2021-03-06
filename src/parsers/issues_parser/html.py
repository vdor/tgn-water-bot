import re
from typing import List

from bs4 import BeautifulSoup

from src.domain import WaterIssue
from src.repositories.issues_html_repository.base import IssuesHTMLRepositoryABC

from .base import IssuesParserABC


class IssuesParserHTML(IssuesParserABC):
    _issues_html_repository: IssuesHTMLRepositoryABC
    _parse_issue_regexp: re.Pattern = re.compile(r"(\d\d?\.\d\d?.\d\d\d?\d?)(.*)")

    def __init__(self, repo: IssuesHTMLRepositoryABC):
        self._issues_html_repository = repo

    async def parse(self) -> List[WaterIssue]:
        html = await self._issues_html_repository.get_html_content()
        bs = BeautifulSoup(html, "html.parser")
        issues = bs.select("tr")
        result: List[WaterIssue] = []

        for issue in issues:
            text = issue.text.strip("\n")
            match = self._parse_issue_regexp.match(text)

            if match is None:
                continue

            groups = match.groups()

            if len(groups) == 2:
                result.append(
                    WaterIssue(
                        date_text=groups[0].strip(),
                        content=groups[1].strip(),
                    )
                )

        return result
