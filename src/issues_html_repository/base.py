import abc


class IssuesHTMLRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def get_html_content(self) -> str:
        raise NotImplementedError
