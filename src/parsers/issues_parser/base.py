import abc
from typing import List

from src.domain import WaterIssue


class IssuesParserABC(abc.ABC):
    @abc.abstractmethod
    async def parse(self) -> List[WaterIssue]:
        raise NotImplementedError
