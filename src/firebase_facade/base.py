import abc

from firebase_admin.db import Reference


class IssuesRefProviderABC(abc.ABC):
    @abc.abstractmethod
    def get_issues_ref(self) -> Reference:
        raise NotImplementedError


class TelegramChatsRefProvider(abc.ABC):
    @abc.abstractmethod
    def get_telegram_ref(self) -> Reference:
        raise NotImplementedError

    @abc.abstractmethod
    def get_telegram_chat_ids_ref(self) -> Reference:
        raise NotImplementedError


class FirebaseFacadeABC(IssuesRefProviderABC, TelegramChatsRefProvider):
    pass
