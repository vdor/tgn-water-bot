import asyncio
import logging
from typing import List

from aiogram import Bot

from src.domain.water_issue import WaterIssue
from src.repositories.issues_repository.base import IssuesRepositoryABC
from src.repositories.telegram_chat_ids_repository.base import TelegramChatIdsRepositoryABC

from .base import IssueSenderABC

logger = logging.getLogger(__name__)


class IssueSenderTelegram(IssueSenderABC):
    _bot: Bot
    _chats_repository: TelegramChatIdsRepositoryABC
    _issue_repository: IssuesRepositoryABC

    def __init__(
        self,
        bot: Bot,
        chats_repo: TelegramChatIdsRepositoryABC,
        issue_repo: IssuesRepositoryABC,
    ):
        self._bot = bot
        self._chats_repository = chats_repo
        self._issue_repository = issue_repo

    async def send(self):
        issues = await self._issue_repository.get_unsent_tg_issues()
        chat_ids = await self._chats_repository.get_all_chats()
        logger.info("sending {%s} issues to {%s} chats", len(issues), len(chat_ids))
        await asyncio.gather(
            *[self._send_issue_to_chats(chat_ids, issue) for issue in issues]
        )
        await self._issue_repository.mark_as_sent_tg_by_hashes(
            [issue.hash for issue in issues]
        )

    async def _send_issue_to_chats(self, chat_ids: List[str], issue: WaterIssue):
        exceptions = await asyncio.gather(
            *[
                self._send_issue_to_chat(chat_id=chat_id, issue=issue)
                for chat_id in chat_ids
            ],
            return_exceptions=True,
        )

        for i, e in enumerate(exceptions):
            if e is Exception:
                logger.error(
                    'error on sending issue to chat "{chat_id}" - "{exception}"',
                    chat_id=chat_ids[i],
                    exception=e,
                )

    async def _send_issue_to_chat(self, chat_id: str, issue: WaterIssue):
        await self._bot.send_message(
            chat_id, issue.formatted, disable_notification=not issue.is_important
        )
