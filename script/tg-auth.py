from config import api_id, api_hash, session_name

from telethon import TelegramClient
import asyncio


client = TelegramClient(session_name, api_id, api_hash)


async def connect_client():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)  # Запросит код подтверждения на ваш номер телефона
        await client.sign_in(phone, input('Введите код: ')) # Введите код, который придет вам в Telegram
    print('Успешно авторизован!')

phone = input('Введите ваш номер телефона: ')

asyncio.run(connect_client())
