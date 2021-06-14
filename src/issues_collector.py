import logging

from src.issues_parser.base import IssuesParserABC
from src.issues_repository.base import IssuesRepositoryABC

logger = logging.getLogger(__name__)


class IssuesCollector:
    parser: IssuesParserABC
    repo: IssuesRepositoryABC

    def __init__(self, parser: IssuesParserABC, repo: IssuesRepositoryABC):
        self.parser = parser
        self.repo = repo

    async def collect(self):
        logger.info("parsing issues")
        issues = await self.parser.parse()
        logger.info("saving issues")
        await self.repo.try_add_issues(issues)
