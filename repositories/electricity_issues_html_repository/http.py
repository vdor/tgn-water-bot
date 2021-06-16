import logging
from datetime import datetime, timedelta
from typing import Optional

import aiohttp
import yarl

from .base import ElectricityIssuesHTMLRepositoryABC

logger = logging.getLogger(__name__)


class ElectricityIssuesHTMLRepositoryHTTP(ElectricityIssuesHTMLRepositoryABC):
    _base_uri: str

    def __init__(self, base_uri: str):
        self._base_uri = base_uri

    async def get_html_content(self, date: Optional[datetime] = None) -> str:
        if date is None:
            date = datetime.now()

        date_to = date + timedelta(days=1)

        date_from_text = date.strftime("%d.%m.%Y")
        date_to_text = date_to.strftime("%d.%m.%Y")
        url = yarl.URL(
            self._base_uri + "&dateFrom=" + date_from_text + "&dateTo=" + date_to_text,
            encoded=True,
        )

        async with aiohttp.ClientSession(
            requote_redirect_url=False, raise_for_status=True
        ) as session:
            async with session.get(url) as resp:
                return await resp.text()
