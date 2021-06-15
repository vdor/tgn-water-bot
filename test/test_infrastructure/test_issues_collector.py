from unittest.mock import AsyncMock, MagicMock

import pytest

from domain import WaterIssue
from infrastructure.issues_collector import IssuesCollector


@pytest.mark.asyncio
async def test_issues_collector():
    water_issues = [WaterIssue(date_text="date", content="content")]
    parser = MagicMock()
    parser.parse = AsyncMock(return_value=water_issues)

    repo = MagicMock()
    repo.try_add_issues = AsyncMock()

    collector = IssuesCollector(parser=parser, repo=repo)
    await collector.collect()

    parser.parse.assert_called_once()
    repo.try_add_issues.assert_called_once_with(water_issues)


@pytest.mark.asyncio
async def test_issues_collector_empty_issues():
    water_issues = [
        WaterIssue(date_text="date", content=""),
        WaterIssue(date_text="date", content="not_empty"),
    ]
    expected_to_save = [water_issues[1]]
    parser = MagicMock()
    parser.parse = AsyncMock(return_value=water_issues)

    repo = MagicMock()
    repo.try_add_issues = AsyncMock()

    collector = IssuesCollector(parser=parser, repo=repo)
    await collector.collect()

    parser.parse.assert_called_once()
    repo.try_add_issues.assert_called_once_with(expected_to_save)
