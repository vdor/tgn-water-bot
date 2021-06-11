from src.issues_parser.base import IssuesParserABC
from src.issues_repository.base import IssuesRepositoryABC


class IssuesCollector:
    parser: IssuesParserABC
    repo: IssuesRepositoryABC

    def __init__(self, parser: IssuesParserABC, repo: IssuesRepositoryABC):
        self.parser = parser
        self.repo = repo

    async def collect(self):
        issues = await self.parser.parse()
        await self.repo.try_add_issues(issues)
