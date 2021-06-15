from typing import List

from repositories.telegram_chat_ids_repository.base import TelegramChatIdsRepositoryABC


class TelegramChatIdsRepositoryLocal(TelegramChatIdsRepositoryABC):
    _filename: str

    def __init__(self, filename: str):
        self._filename = filename

    async def get_all_chats(self) -> List[str]:
        with open(self._filename, "r") as f:
            line = f.readline()
            return line.split(",")

    async def add_chat(self, chat_id: str):
        with open(self._filename, "a") as f:
            f.write(f"{chat_id},")

    async def remove_chat(self, chat_id: str):
        chats = await self.get_all_chats()
        filtered = filter(lambda id_: id_ != chat_id, chats)
        self.set_chats(list(filtered))

    def set_chats(self, chat_ids: List[str]):
        with open(self._filename, "w") as f:
            f.write(",".join(chat_ids))

    async def is_chat_id_subscribed(self, chat_id: str) -> bool:
        with open(self._filename, "r") as f:
            ids = f.readline().split(",")
            return chat_id in ids
