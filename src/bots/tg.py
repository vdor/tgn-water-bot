from aiogram import Bot, Dispatcher, types

from src.telegram_chat_ids_repository.base import TelegramChatIdsRepositoryABC


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
            await dispatcher.start_polling()
        finally:
            await bot.close()

    async def chat_member_handler(self, event: types.ChatMemberUpdated):
        old_member = event.old_chat_member
        new_member = event.new_chat_member
        if old_member.status == types.ChatMemberStatus.MEMBER and new_member.status != types.ChatMemberStatus.MEMBER:
            await self._chats_repo.remove_chat(str(event.chat.id))
        elif old_member.status != types.ChatMemberStatus.MEMBER and new_member.status == types.ChatMemberStatus.MEMBER:
            await self._chats_repo.add_chat(str(event.chat.id))
