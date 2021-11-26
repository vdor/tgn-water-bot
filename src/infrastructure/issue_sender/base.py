import abc


class IssueSenderABC(abc.ABC):
    @abc.abstractmethod
    async def send(self):
        raise NotImplementedError
