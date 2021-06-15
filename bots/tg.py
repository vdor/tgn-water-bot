import logging

from aiogram import Dispatcher, types
from aiogram.types import AllowedUpdates, ChatMemberStatus

from repositories.telegram_chat_ids_repository.base import TelegramChatIdsRepositoryABC

logger = logging.getLogger(__name__)


class TelegramBot:
    _chats_repo: TelegramChatIdsRepositoryABC
    _dispatcher: Dispatcher
    _relax: int

    def __init__(
        self, dispatcher: Dispatcher, chats_repo: TelegramChatIdsRepositoryABC, relax=5
    ):
        self._dispatcher = dispatcher
        self._chats_repo = chats_repo
        self._relax = relax

    async def start(self):
        try:
            self._dispatcher.register_my_chat_member_handler(self.chat_member_handler)
            self._dispatcher.register_message_handler(
                self.start_message_handler, commands="start"
            )
            await self._dispatcher.start_polling(
                allowed_updates=AllowedUpdates.MESSAGE + AllowedUpdates.MY_CHAT_MEMBER,
                relax=self._relax,
            )
        finally:
            await self._dispatcher.bot.close()

    async def chat_member_handler(self, event: types.ChatMemberUpdated):
        new_status = event.new_chat_member.status
        logger.info(
            'chat member status changed to "{%s}" in the chat "{%s}"',
            new_status,
            event.chat.id,
        )

        if ChatMemberStatus.is_chat_member(new_status):
            await self._chats_repo.add_chat(str(event.chat.id))
        else:
            await self._chats_repo.remove_chat(str(event.chat.id))

    async def start_message_handler(self, message: types.Message):
        chat_id = str(message.chat.id)
        logger.info('got a start command in the chat "{%s}"', chat_id)

        is_subscribed = await self._chats_repo.is_chat_id_subscribed(chat_id)
        if not is_subscribed:
            await self._chats_repo.add_chat(chat_id)
            await message.answer("Готово! Сообщу о проблемах с водой в городе 👌")
        else:
            await message.answer("Когда будут проблемы - сообщу!")
