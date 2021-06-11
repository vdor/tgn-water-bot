import aiohttp

from .base import IssuesHTMLRepositoryABC
from .exceptions import LoadingHTMLIssuesException


class IssuesHTMLRepositoryHTTP(IssuesHTMLRepositoryABC):
    _uri: str

    def __init__(self, uri: str):
        self._uri = uri

    async def get_html_content(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self._uri) as resp:
                if resp.status != 200:
                    raise LoadingHTMLIssuesException
                return await resp.text()
