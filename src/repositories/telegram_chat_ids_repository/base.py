import abc
from typing import List


class TelegramChatIdsRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def get_all_chats(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_chat(self, chat_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_chat(self, chat_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def is_chat_id_subscribed(self, chat_id: str) -> bool:
        raise NotImplementedError
