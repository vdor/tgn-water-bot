import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberStatus, AllowedUpdates

from src.telegram_chat_ids_repository.base import TelegramChatIdsRepositoryABC

logger = logging.getLogger(__name__)


class TelegramBot:
    _bot_token: str
    _chats_repo: TelegramChatIdsRepositoryABC

    def __init__(self, token: str, chats_repo: TelegramChatIdsRepositoryABC):
        self._bot_token = token
        self._chats_repo = chats_repo

    async def start(self):
        bot = Bot(token=self._bot_token)
        try:
            dispatcher = Dispatcher(bot=bot)
            dispatcher.register_my_chat_member_handler(self.chat_member_handler)
            dispatcher.register_message_handler(self.start_message_handler, commands='start')
            await dispatcher.start_polling(allowed_updates=AllowedUpdates.MESSAGE + AllowedUpdates.MY_CHAT_MEMBER,
                                           relax=5)
        finally:
            await bot.close()

    async def chat_member_handler(self, event: types.ChatMemberUpdated):
        new_status = event.new_chat_member.status
        logger.info('chat member status changed to "{%s}" in the chat "{%s}"', new_status, event.chat.id)

        if ChatMemberStatus.is_chat_member(new_status):
            await self._chats_repo.add_chat(str(event.chat.id))
        else:
            await self._chats_repo.remove_chat(str(event.chat.id))

    async def start_message_handler(self, message: types.Message):
        logger.info('got a start command in the chat "{%s}"', message.chat.id)
        await self._chats_repo.add_chat(str(message.chat.id))
