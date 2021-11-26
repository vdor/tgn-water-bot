from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain import WaterIssue
from src.infrastructure.issue_sender.telegram import IssueSenderTelegram


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

    bot.send_message.assert_called_once_with(
        chats[0],
        water_issues[0].formatted,
        disable_notification=False,
    )
    issue_repo.mark_as_sent_tg_by_hashes.assert_called_once_with([water_issues[0].hash])


@pytest.mark.asyncio
async def test_send_disable_notifications():
    chat_id = "1"

    chats_repo = MagicMock()
    chats_repo.get_all_chats = AsyncMock(return_value=[chat_id])

    issue_repo = MagicMock()
    issue_repo.mark_as_sent_tg_by_hashes = AsyncMock()

    bot = MagicMock()

    sender = IssueSenderTelegram(chats_repo=chats_repo, issue_repo=issue_repo, bot=bot)

    # check important
    water_issues_important = MagicMock()
    water_issues_important.is_important = True

    issue_repo.get_unsent_tg_issues = AsyncMock(return_value=[water_issues_important])
    bot.send_message = AsyncMock()
    await sender.send()
    bot.send_message.assert_called_with(
        chat_id,
        water_issues_important.formatted,
        disable_notification=False,
    )

    # check not important
    water_issues_not_important = MagicMock()
    water_issues_not_important.is_important = False

    issue_repo.get_unsent_tg_issues = AsyncMock(
        return_value=[water_issues_not_important]
    )
    bot.send_message = AsyncMock()
    await sender.send()
    bot.send_message.assert_called_with(
        chat_id,
        water_issues_not_important.formatted,
        disable_notification=True,
    )
