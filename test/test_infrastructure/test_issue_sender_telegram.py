from unittest.mock import AsyncMock, MagicMock

import pytest

from domain import WaterIssue
from infrastructure.issue_sender.telegram import IssueSenderTelegram


@pytest.mark.asyncio
async def test_send():
    water_issues = [WaterIssue(content="useful content", date_text="01")]
    chats = ["1"]

    chats_repo = MagicMock()
    chats_repo.get_all_chats = AsyncMock(return_value=chats)

    issue_repo = MagicMock()
    issue_repo.get_unsent_tg_issues = AsyncMock(return_value=water_issues)
    issue_repo.mark_as_sent_tg_by_hashes = AsyncMock()

    bot = MagicMock()
    bot.send_message = AsyncMock()

    sender = IssueSenderTelegram(chats_repo=chats_repo, issue_repo=issue_repo, bot=bot)
    await sender.send()

    bot.send_message.assert_called_once_with(chats[0], water_issues[0].formatted)
    issue_repo.mark_as_sent_tg_by_hashes.assert_called_once_with([water_issues[0].hash])
