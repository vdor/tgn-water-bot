import abc
from typing import List

from src.domain import WaterIssue


class IssuesRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def get_unsent_tg_issues(self) -> List[WaterIssue]:
        raise NotImplementedError

    @abc.abstractmethod
    async def mark_as_sent_tg_by_hashes(self, issue_hashes: List[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def try_add_issues(self, issues: List[WaterIssue]):
        raise NotImplementedError
