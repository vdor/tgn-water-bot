from typing import List

from firebase_admin.db import Reference

from firebase_facade.base import TelegramChatsRefProvider
from repositories.telegram_chat_ids_repository.base import TelegramChatIdsRepositoryABC


class TelegramChatIdsRepositoryFirebase(TelegramChatIdsRepositoryABC):
    _ref_provider: TelegramChatsRefProvider

    def __init__(self, ref_provider: TelegramChatsRefProvider):
        self._ref_provider = ref_provider

    @property
    def _ref(self) -> Reference:
        return self._ref_provider.get_telegram_chat_ids_ref()

    async def get_all_chats(self) -> List[str]:
        ids = self._ref.order_by_child("active").equal_to(True).get()

        if ids is None:
            return []

        return ids  # noqa

    async def add_chat(self, chat_id: str):
        self._ref.child(chat_id).set({"active": True})

    async def remove_chat(self, chat_id: str):
        self._ref.child(chat_id).set({"active": False})

    async def is_chat_id_subscribed(self, chat_id: str) -> bool:
        data = self._ref.child(chat_id).get()

        if isinstance(data, dict):
            return data.get("active", False)

        return False
