from unittest.mock import AsyncMock, MagicMock

import pytest

from parsers.issues_parser.html import IssuesParserHTML


@pytest.mark.asyncio
async def test_parse():
    html_repo = MagicMock()
    with open("test/test_parsers/mocked_html.html") as f:
        mocked_html = f.read()

    html_repo.get_html_content = AsyncMock(return_value=mocked_html)

    parser = IssuesParserHTML(repo=html_repo)
    issues = await parser.parse()

    assert issues[0].content == "Something useful"
    assert issues[0].date_text == "09.06.2021"
    assert issues[0].is_sent_telegram is False

    assert issues[1].content == "Something other"
    assert issues[1].date_text == "10.06.2021"
    assert issues[1].is_sent_telegram is False

    assert len(issues) == 2
