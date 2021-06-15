from unittest.mock import MagicMock

import pytest

from repositories.telegram_chat_ids_repository.firebase import (
    TelegramChatIdsRepositoryFirebase,
)


@pytest.mark.asyncio
async def test_firebase_get_all_chats():
    expected_chats = ["a", "b"]

    reference = MagicMock()
    reference.child().child().order_by_child().equal_to().get.return_value = (
        expected_chats
    )
    repo = TelegramChatIdsRepositoryFirebase(reference=reference)
    chats = await repo.get_all_chats()
    assert chats == expected_chats

    reference.child.assert_called_with("telegram")
    reference.child().child.assert_called_with("active_chat_ids")
    reference.child().child().order_by_child.assert_called_with("active")
    reference.child().child().order_by_child().equal_to.assert_called_with(True)


@pytest.mark.asyncio
async def test_firebase_get_all_chats_no_chats():
    reference = MagicMock()
    reference.child().child().order_by_child().equal_to().get.return_value = None
    repo = TelegramChatIdsRepositoryFirebase(reference=reference)
    result = await repo.get_all_chats()
    assert len(result) == 0

    reference.child.assert_called_with("telegram")
    reference.child().child.assert_called_with("active_chat_ids")


@pytest.mark.asyncio
async def test_firebase_add_chat():
    chat_id = "1"

    reference = MagicMock()
    repo = TelegramChatIdsRepositoryFirebase(reference=reference)

    await repo.add_chat(chat_id)

    reference.child.assert_called_with("telegram")
    reference.child("telegram").child.assert_called_with("active_chat_ids")
    reference.child("telegram").child("active_chat_ids").child.assert_called_once_with(
        chat_id
    )
    reference.child("telegram").child("active_chat_ids").child(
        chat_id
    ).set.assert_called_once_with({"active": True})


@pytest.mark.asyncio
async def test_firebase_remove_chat():
    chat_id = "1"

    reference = MagicMock()
    repo = TelegramChatIdsRepositoryFirebase(reference=reference)

    await repo.remove_chat(chat_id)

    reference.child.assert_called_with("telegram")
    reference.child("telegram").child.assert_called_with("active_chat_ids")
    reference.child("telegram").child("active_chat_ids").child.assert_called_once_with(
        chat_id
    )
    reference.child("telegram").child("active_chat_ids").child(
        chat_id
    ).set.assert_called_once_with({"active": False})


@pytest.mark.asyncio
async def test_firebase_is_chat_id_subscribed_true():
    chat_id = "1"

    reference = MagicMock()
    reference.child("telegram").child("active_chat_ids").child(
        chat_id
    ).get.return_value = {"active": True}
    repo = TelegramChatIdsRepositoryFirebase(reference=reference)

    result = await repo.is_chat_id_subscribed(chat_id)
    assert result is True


@pytest.mark.asyncio
async def test_firebase_is_chat_id_subscribed_none():
    chat_id = "1"

    reference = MagicMock()
    reference.child("telegram").child("active_chat_ids").child(
        chat_id
    ).get.return_value = None
    repo = TelegramChatIdsRepositoryFirebase(reference=reference)

    result = await repo.is_chat_id_subscribed(chat_id)
    assert result is False
