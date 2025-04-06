from config import api_id, api_hash, session_name

from telethon import TelegramClient


client = TelegramClient(session_name, api_id, api_hash)
phone = None


async def connect_client():
    global phone
    await client.connect()
    if not await client.is_user_authorized():
        phone = input('Введите ваш номер телефона: ')
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Введите код из Telegram: '))
    print('Успешно авторизован в Telegram!')
