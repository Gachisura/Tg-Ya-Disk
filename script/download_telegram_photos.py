from config import api_id, api_hash, session_name
from tg_auth import client
from telethon import TelegramClient
import asyncio
import os
from tqdm.asyncio import tqdm


async def download_photos_from_chat(chat_id):
    """Скачивает все фотографии из указанного чата Telegram."""
    if not client.is_connected:
        print("Клиент Telegram не подключен. Пожалуйста, запустите авторизацию.")
        return

    print(f'\nПолучение сообщений из чата Telegram с ID: {chat_id}')
    total_photos = 0
    async for message in client.iter_messages(chat_id):
        if message.photo:
            total_photos += 1

    print(f'Найдено {total_photos} фотографий для загрузки.')
    downloaded_count = 0
    photos_dir = 'photos'
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
    async for message in tqdm(client.iter_messages(chat_id), total=total_photos, desc="Загрузка фото"):
        if message.photo:
            file_path = await client.download_media(message.photo, file=photos_dir)
            if file_path:
                downloaded_count += 1
    print(f'Загружено {downloaded_count} фотографий в папку "{photos_dir}/".')
