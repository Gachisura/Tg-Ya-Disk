from config import api_id, api_hash, session_name
from telethon import TelegramClient, utils
import asyncio


from telethon import TelegramClient, utils
from tg_auth import client


async def get_dialogs():
    """Получает и выводит список диалогов Telegram."""
    if not client.is_connected:
        print("Клиент Telegram не подключен. Пожалуйста, запустите авторизацию.")
        return

    dialogs = await client.get_dialogs()
    print('\nВаши диалоги Telegram:')
    for i, dialog in enumerate(dialogs):
        entity = dialog.entity
        name = utils.get_display_name(entity)
        chat_type = 'Unknown'
        if hasattr(entity, 'title'):
            chat_type = 'Группа/Канал'
        elif hasattr(entity, 'first_name'):
            chat_type = 'Личный чат'
        print(f'{i+1}. {name} ({chat_type}), ID: {entity.id}')
