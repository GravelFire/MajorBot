from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from bot.config import settings
from bot.utils import logger


async def register_sessions() -> None:
    API_ID = settings.API_ID
    API_HASH = settings.API_HASH

    if not API_ID or not API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    session_name = input('\nEnter the session name (press Enter to exit): ')

    if not session_name:
        return None

    session = TelegramClient(
        f'sessions/{session_name}',
        api_id=API_ID,
        api_hash=API_HASH,
        system_version='Windows 11'
    )

    await session.start(password=lambda: input('Please enter your password: '))

    user_data = await session.get_me()

    logger.success(f'Session added successfully @{user_data.username} | {user_data.first_name} {user_data.last_name}')