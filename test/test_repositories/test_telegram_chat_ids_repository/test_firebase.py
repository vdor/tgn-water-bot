from unittest.mock import MagicMock

import pytest

from src.repositories.telegram_chat_ids_repository.firebase import (
    TelegramChatIdsRepositoryFirebase,
)


@pytest.mark.asyncio
async def test_firebase_get_all_chats():
    expected_chats = ["a", "b"]

    ref_provider = MagicMock()
    ref_provider.get_telegram_chat_ids_ref().order_by_child().equal_to().get.return_value = (
        expected_chats
    )
    repo = TelegramChatIdsRepositoryFirebase(ref_provider=ref_provider)
    chats = await repo.get_all_chats()
    assert chats == expected_chats

    ref_provider.get_telegram_chat_ids_ref().order_by_child.assert_called_with("active")
    ref_provider.get_telegram_chat_ids_ref().order_by_child().equal_to.assert_called_with(
        True
    )


@pytest.mark.asyncio
async def test_firebase_get_all_chats_no_chats():
    ref_provider = MagicMock()
    ref_provider.get_telegram_chat_ids_ref().order_by_child().equal_to().get.return_value = (
        None
    )
    repo = TelegramChatIdsRepositoryFirebase(ref_provider=ref_provider)
    result = await repo.get_all_chats()
    assert len(result) == 0


@pytest.mark.asyncio
async def test_firebase_add_chat():
    chat_id = "1"

    ref_provider = MagicMock()
    repo = TelegramChatIdsRepositoryFirebase(ref_provider=ref_provider)

    await repo.add_chat(chat_id)

    ref_provider.get_telegram_chat_ids_ref().child.assert_called_once_with(chat_id)
    ref_provider.get_telegram_chat_ids_ref().child(chat_id).set.assert_called_once_with(
        {"active": True}
    )


@pytest.mark.asyncio
async def test_firebase_remove_chat():
    chat_id = "1"

    ref_provider = MagicMock()
    repo = TelegramChatIdsRepositoryFirebase(ref_provider=ref_provider)

    await repo.remove_chat(chat_id)

    ref_provider.get_telegram_chat_ids_ref().child.assert_called_once_with(chat_id)
    ref_provider.get_telegram_chat_ids_ref().child(chat_id).set.assert_called_once_with(
        {"active": False}
    )


@pytest.mark.asyncio
async def test_firebase_is_chat_id_subscribed_true():
    chat_id = "1"

    ref_provider = MagicMock()
    ref_provider.get_telegram_chat_ids_ref().child(chat_id).get.return_value = {
        "active": True
    }
    repo = TelegramChatIdsRepositoryFirebase(ref_provider=ref_provider)

    result = await repo.is_chat_id_subscribed(chat_id)
    assert result is True


@pytest.mark.asyncio
async def test_firebase_is_chat_id_subscribed_none():
    chat_id = "1"

    ref_provider = MagicMock()
    ref_provider.get_telegram_chat_ids_ref().child(chat_id).get.return_value = None
    repo = TelegramChatIdsRepositoryFirebase(ref_provider=ref_provider)

    result = await repo.is_chat_id_subscribed(chat_id)
    assert result is False
