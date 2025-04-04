from config import api_id, api_hash, session_name
from telethon import TelegramClient, events, utils
import asyncio


async def get_dialogs():
    """Скрипт для получения списка чатов, запускается из командной строки"""
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        print("Пожалуйста, авторизуйтесь сначала.")
        await client.disconnect()
        return

    dialogs = await client.get_dialogs()
    print('Ваши диалоги:')
    for i, dialog in enumerate(dialogs):
        entity = dialog.entity
        name = utils.get_display_name(entity)
        chat_type = 'Unknown'
        if hasattr(entity, 'title'):
            chat_type = 'Группа/Канал'
        elif hasattr(entity, 'first_name'):
            chat_type = 'Личный чат'
        print(f'{i+1}. {name} ({chat_type}), ID: {entity.id}')

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(get_dialogs())
