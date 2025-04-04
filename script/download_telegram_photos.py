from config import api_id, api_hash, session_name
from telethon import TelegramClient
import asyncio
import os
from tqdm.asyncio import tqdm


async def download_photos_from_chat(chat_id):
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        print("Пожалуйста, авторизуйтесь сначала.")
        await client.disconnect()
        return

    print(f'Получение сообщений из чата с ID: {chat_id}')
    total_photos = 0
    async for message in client.iter_messages(chat_id):
        if message.photo:
            total_photos += 1

    print(f'Найдено {total_photos} фотографий для загрузки.')
    downloaded_count = 0
    async for message in tqdm(client.iter_messages(chat_id), total=total_photos, desc="Загрузка фото"):
        if message.photo:
            file_path = await client.download_media(message.photo, file='photos/')
            if file_path:
                downloaded_count += 1
    print(f'Загружено {downloaded_count} фотографий в папку "photos/".')

    await client.disconnect()

if __name__ == '__main__':
    if not os.path.exists('photos'):
        os.makedirs('photos')

    target_chat_id_input = input("Введите ID чата, из которого вы хотите скачать фотографии: ")
    try:
        target_chat_id = int(target_chat_id_input)
        asyncio.run(download_photos_from_chat(target_chat_id))
    except ValueError:
        print("Некорректный ID чата. Пожалуйста, введите целое число.")
