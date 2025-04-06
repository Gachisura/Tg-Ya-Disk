import asyncio
from config import client_id_ya, client_secret_ya
from tg_auth import connect_client, client
from list_chats import get_dialogs
from download_telegram_photos import download_photos_from_chat
from get_yandex_token import get_oauth_token
from upload_to_yadisk import upload_photos_to_yadisk, create_yandex_disk_folder_async
import aiohttp


async def main():
    print("Добро пожаловать в скрипт для работы с Telegram и Яндекс Диском!")

    # Авторизация в Telegram
    await connect_client()
    if not await client.is_user_authorized():
        return

    while True:
        print("\nВыберите действие:")
        print("1. Получить список диалогов Telegram")
        print("2. Скачать фотографии из чата Telegram")
        print("3. Загрузить фотографии из папки 'photos/' на Яндекс Диск")
        print("4. Создать папку на Яндекс Диске")
        print("5. Получить новый OAuth-токен Яндекс Диска")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            await get_dialogs()
        elif choice == '2':
            chat_id_input = input("Введите ID чата для скачивания фотографий: ")
            try:
                chat_id = int(chat_id_input)
                await download_photos_from_chat(chat_id)
            except ValueError:
                print("Некорректный ID чата. Пожалуйста, введите целое число.")
        elif choice == '3':
            await upload_photos_to_yadisk()
        elif choice == '4':
            folder_name = input("Введите имя папки для создания на Яндекс Диске "
                                "(например, /Мои документы/Новая папка): ")
            async with aiohttp.ClientSession() as session:
                await create_yandex_disk_folder_async(session, folder_name)
        elif choice == '5':
            print("\nДля получения нового OAuth-токена Яндекс Диска:")
            print(f"1. Перейдите по следующей ссылке, авторизуйтесь и скопируйте полученный Auth Code:")
            print(f"   https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id_ya}")
            new_auth_code = input("2. Введите полученный Auth Code: ")
            if new_auth_code:
                access_token, refresh_token = get_oauth_token(client_id_ya, client_secret_ya, new_auth_code)
                if access_token:
                    print(f"\nВаш новый Access Token (YA_DISK_TOKEN): {access_token}")
                    print("Пожалуйста, обновите эту переменную в вашем файле .env или config.py.")
                if refresh_token:
                    print(f"Ваш Refresh Token: {refresh_token}")
                    print("Рекомендуется сохранить его для обновления Access Token в будущем.")
            else:
                print("Вы не ввели Auth Code.")
        elif choice == '6':
            await client.disconnect()
            print("Выход из скрипта.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")

if __name__ == '__main__':
    asyncio.run(main())
