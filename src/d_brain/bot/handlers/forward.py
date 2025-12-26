"""Forwarded message handler."""

import logging
from datetime import datetime

from aiogram import Router
from aiogram.types import Message

from d_brain.config import get_settings
from d_brain.services.storage import VaultStorage

router = Router(name="forward")
logger = logging.getLogger(__name__)


@router.message(lambda m: m.forward_origin is not None)
async def handle_forward(message: Message) -> None:
    """Handle forwarded messages."""
    if not message.from_user:
        return

    settings = get_settings()
    storage = VaultStorage(settings.vault_path)

    # Determine source name
    source_name = "Unknown"
    origin = message.forward_origin

    if hasattr(origin, "sender_user") and origin.sender_user:
        user = origin.sender_user
        source_name = user.full_name
    elif hasattr(origin, "sender_user_name") and origin.sender_user_name:
        source_name = origin.sender_user_name
    elif hasattr(origin, "chat") and origin.chat:
        chat = origin.chat
        source_name = f"@{chat.username}" if chat.username else chat.title or "Channel"
    elif hasattr(origin, "sender_name") and origin.sender_name:
        source_name = origin.sender_name

    content = message.text or message.caption or "[media]"
    msg_type = f"[forward from: {source_name}]"

    timestamp = datetime.fromtimestamp(message.date.timestamp())
    storage.append_to_daily(content, timestamp, msg_type)

    await message.answer(f"✓ Сохранено (от {source_name})")
    logger.info("Forwarded message saved from: %s", source_name)
