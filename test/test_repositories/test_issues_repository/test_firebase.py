from typing import Dict
from unittest.mock import MagicMock

import pytest

from src.domain import WaterIssue
from src.repositories.issues_repository.firebase import IssuesRepositoryFirebase


@pytest.mark.asyncio
async def test_firebase_get_unsent_tg_issues():
    water_issues = {
        "hash_1": {
            "date_text": "date",
            "content": "content",
        },
    }

    expected_issues = [
        WaterIssue(
            date_text=water_issues["hash_1"]["date_text"],
            content=water_issues["hash_1"]["content"],
        )
    ]

    ref_provider = MagicMock()
    ref_provider.get_issues_ref().order_by_child().equal_to().get.return_value = (
        water_issues
    )

    repo = IssuesRepositoryFirebase(ref_provider=ref_provider)
    result = await repo.get_unsent_tg_issues()
    assert result == expected_issues

    ref_provider.get_issues_ref().order_by_child.assert_called_with("is_sent_telegram")
    ref_provider.get_issues_ref().order_by_child().equal_to.assert_called_with(False)


@pytest.mark.asyncio
async def test_firebase_mark_as_sent_tg_by_hashes():
    hashes = ["1a", "1b"]
    ref_provider = MagicMock()
    repo = IssuesRepositoryFirebase(ref_provider=ref_provider)
    await repo.mark_as_sent_tg_by_hashes(hashes)

    expected_payload = {
        "1a/is_sent_telegram": True,
        "1b/is_sent_telegram": True,
    }
    ref_provider.get_issues_ref().update.assert_called_once_with(expected_payload)


@pytest.mark.asyncio
async def test_firebase_mark_as_sent_tg_by_hashes_no_hashes():
    hashes = []
    ref_provider = MagicMock()
    repo = IssuesRepositoryFirebase(ref_provider=ref_provider)
    await repo.mark_as_sent_tg_by_hashes(hashes)
    ref_provider.get_issues_ref().update.assert_not_called()


@pytest.mark.asyncio
async def test_firebase_try_add_issues():
    issues = [
        WaterIssue(
            date_text="date_text",
            content="already_added",
        ),
        WaterIssue(
            date_text="date_text",
            content="not_added",
        ),
    ]

    # map mocked refs with issues to hashes
    issue_refs: Dict[str, MagicMock] = {
        issues[0].hash: MagicMock(),
        issues[1].hash: MagicMock(),
    }
    issue_refs[issues[0].hash].get.return_value = issues[0]
    # set return value as None to because this issue is not added
    issue_refs[issues[1].hash].get.return_value = None

    def get_by_hash(h: str):
        return issue_refs[h]

    ref_provider = MagicMock()
    ref_provider.get_issues_ref().child.side_effect = get_by_hash
    repo = IssuesRepositoryFirebase(ref_provider=ref_provider)
    await repo.try_add_issues(issues)
    issue_refs[issues[1].hash].set.assert_called_once_with(issues[1].asdict)
