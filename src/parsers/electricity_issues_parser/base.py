import abc
from typing import List

from src.domain import ElectricityIssue


class ElectricityIssuesParserABC(abc.ABC):
    @abc.abstractmethod
    async def parse(self) -> List[ElectricityIssue]:
        raise NotImplementedError
