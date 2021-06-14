from typing import List

from firebase_admin.db import Reference

from src.telegram_chat_ids_repository.base import TelegramChatIdsRepositoryABC


class TelegramChatIdsRepositoryFirebase(TelegramChatIdsRepositoryABC):
    _reference: Reference

    def __init__(self, reference: Reference):
        self._reference = reference

    @property
    def _telegram_ref(self):
        return self._reference.child('telegram')

    @property
    def _active_chat_ids_ref(self):
        return self._telegram_ref.child('active_chat_ids')

    async def get_all_chats(self) -> List[str]:
        ids = self._active_chat_ids_ref.order_by_child('active').equal_to(True).get()

        if ids is None:
            return []

        return ids # noqa

    async def add_chat(self, chat_id: str):
        self._active_chat_ids_ref.child(chat_id).set({'active': True})

    async def remove_chat(self, chat_id: str):
        self._active_chat_ids_ref.child(chat_id).set({'active': False})

    async def is_chat_id_subscribed(self, chat_id: str) -> bool:
        return self._active_chat_ids_ref.child(chat_id).get() is not None
