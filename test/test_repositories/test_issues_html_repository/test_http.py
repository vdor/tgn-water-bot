from unittest.mock import AsyncMock, MagicMock

import pytest

from src.repositories.issues_html_repository.http import IssuesHTMLRepositoryHTTP


@pytest.mark.asyncio
async def test_a(monkeypatch: pytest.MonkeyPatch):
    mock_response = MagicMock()
    mock_response.__aenter__.return_value = mock_response
    mock_response.__aexit__.return_value = mock_response
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value="content")
    mock_get = MagicMock(return_value=mock_response)

    monkeypatch.setattr("aiohttp.ClientSession.get", mock_get)

    repo = IssuesHTMLRepositoryHTTP(uri="uri")
    result = await repo.get_html_content()
    assert result == "content"
