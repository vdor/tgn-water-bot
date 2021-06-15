from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from aiogram.types import AllowedUpdates, ChatMemberStatus

from bots.tg import TelegramBot


@pytest.fixture
def dispatcher():
    dispatcher = MagicMock()

    dispatcher.start_polling = AsyncMock()
    dispatcher.bot.close = AsyncMock()
    return dispatcher


@pytest.fixture
def chats_repo():
    chats_repo_mock = MagicMock()
    return chats_repo_mock


@pytest.mark.asyncio
async def test_tg_start(dispatcher: Mock, chats_repo: Mock):
    relax_time = 10

    bot = TelegramBot(dispatcher=dispatcher, chats_repo=chats_repo, relax=relax_time)
    await bot.start()

    dispatcher.register_my_chat_member_handler.assert_called_once_with(
        bot.chat_member_handler
    )
    dispatcher.register_message_handler.assert_called_once_with(
        bot.start_message_handler, commands="start"
    )
    dispatcher.start_polling.assert_called_once_with(
        allowed_updates=AllowedUpdates.MESSAGE + AllowedUpdates.MY_CHAT_MEMBER,
        relax=relax_time,
    )
    dispatcher.bot.close.assert_called_once()


@pytest.mark.asyncio
async def test_tg_chat_member_handler_added_to_chat(dispatcher, chats_repo):
    chat_id = 5
    chat_ids_str = "5"

    bot = TelegramBot(dispatcher=dispatcher, chats_repo=chats_repo)

    chat_member_statuses = [
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,
        ChatMemberStatus.RESTRICTED,
    ]

    for status in chat_member_statuses:
        chats_repo.add_chat = AsyncMock()
        chats_repo.remove_chat = AsyncMock()

        event = MagicMock()
        event.new_chat_member.status = status
        event.chat.id = chat_id
        await bot.chat_member_handler(event)
        chats_repo.add_chat.assert_called_once_with(chat_ids_str)
        chats_repo.remove_chat.assert_not_called()


@pytest.mark.asyncio
async def test_tg_chat_member_handler_left_chat(dispatcher: Mock, chats_repo: Mock):
    chat_id = 5
    chat_ids_str = "5"

    bot = TelegramBot(dispatcher=dispatcher, chats_repo=chats_repo)

    left_statuses = [
        ChatMemberStatus.LEFT,
        ChatMemberStatus.KICKED,
    ]

    for status in left_statuses:
        chats_repo.add_chat = AsyncMock()
        chats_repo.remove_chat = AsyncMock()

        event = MagicMock()
        event.new_chat_member.status = status
        event.chat.id = chat_id
        await bot.chat_member_handler(event)
        chats_repo.remove_chat.assert_called_once_with(chat_ids_str)
        chats_repo.add_chat.assert_not_called()


@pytest.mark.asyncio
async def test_tg_start_message_handler_first_message(
    dispatcher: Mock, chats_repo: Mock
):
    chat_id = 5
    chat_ids_str = "5"

    chats_repo.is_chat_id_subscribed = AsyncMock(return_value=False)
    chats_repo.add_chat = AsyncMock()

    message = MagicMock()
    message.chat.id = chat_id
    message.answer = AsyncMock()

    bot = TelegramBot(dispatcher=dispatcher, chats_repo=chats_repo)

    await bot.start_message_handler(message)
    chats_repo.add_chat.assert_called_once_with(chat_ids_str)
    message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_tg_start_message_handler_second_message(
    dispatcher: Mock, chats_repo: Mock
):
    chats_repo.is_chat_id_subscribed = AsyncMock(return_value=True)
    chats_repo.add_chat = AsyncMock()

    message = MagicMock()
    message.chat.id = 5
    message.answer = AsyncMock()

    bot = TelegramBot(dispatcher=dispatcher, chats_repo=chats_repo)

    await bot.start_message_handler(message)
    chats_repo.add_chat.assert_not_called()
    message.answer.assert_called_once()
