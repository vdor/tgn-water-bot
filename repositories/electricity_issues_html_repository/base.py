import abc


class ElectricityIssuesHTMLRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def get_html_content(self) -> str:
        raise NotImplementedError
