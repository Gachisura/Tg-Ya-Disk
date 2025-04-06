from config import ya_disk_token
import aiohttp
import asyncio
import os
from tqdm.asyncio import tqdm


async def create_yandex_disk_folder_async(session, disk_path):
    """Асинхронно создает папку на Яндекс Диске, если она не существует."""
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {'Authorization': f'OAuth {ya_disk_token}'}
    params = {"path": disk_path}

    try:
        async with session.put(url, headers=headers, params=params) as response:
            response.raise_for_status()
            print(f"Папка '{disk_path}' успешно создана на Яндекс Диске.")
            return True
    except aiohttp.ClientResponseError as e:
        if e.status == 409:
            print(f"Папка '{disk_path}' уже существует на Яндекс Диске.")
            return True
        else:
            print(f"Ошибка при создании папки '{disk_path}': {e}")
            print(f"Код ответа: {e.status}")
            print(f"Тело ответа: {await response.text()}")
            return False
    except aiohttp.ClientError as e:
        print(f"Ошибка AIOHTTP при создании папки '{disk_path}': {e}")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при создании папки '{disk_path}': {e}")
        return False


async def upload_to_yandex_disk_async(session, file_path, disk_path):
    """Асинхронно загружает файл по указанному пути на Яндекс Диск."""
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Authorization': f'OAuth {ya_disk_token}'}
    params = {"path": disk_path, "overwrite": "true"}

    try:
        async with session.get(upload_url, headers=headers, params=params) as response:
            response.raise_for_status()
            upload_data = await response.json()
            upload_link = upload_data.get('href')

            if not upload_link:
                print(f"Не удалось получить ссылку для загрузки файла: {file_path}")
                print(f"Тело ответа (GET): {await response.text()}")
                return False

            with open(file_path, 'rb') as f:
                async with session.put(upload_link,
                                       headers={'Content-Type': 'application/octet-stream'},
                                       data=f) as upload_response:
                    upload_response.raise_for_status()
                    return True
    except aiohttp.ClientError as e:
        print(f"Ошибка AIOHTTP при загрузке файла '{os.path.basename(file_path)}': {e}")
        return False
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при загрузке '{os.path.basename(file_path)}': {e}")
        return False


async def upload_photos_to_yadisk():
    """Загружает все фотографии из папки 'photos/' на Яндекс Диск в папку '/TelegramPhotos/'."""
    photos_dir = 'photos'
    disk_folder = '/TelegramPhotos'

    async with aiohttp.ClientSession() as session:
        if await create_yandex_disk_folder_async(session, disk_folder):
            if os.path.exists(photos_dir):
                photo_files = [os.path.join(photos_dir, f)
                               for f in os.listdir(photos_dir)
                               if os.path.isfile(os.path.join(photos_dir, f))]
                if photo_files:
                    print(f"\nНайдено {len(photo_files)} фотографий для загрузки на Яндекс Диск.")
                    tasks = [upload_to_yandex_disk_async(session, photo_file,
                                                         f'{disk_folder}/{os.path.basename(photo_file)}')
                             for photo_file in photo_files]

                    for future in tqdm(asyncio.as_completed(tasks),
                                       total=len(tasks),
                                       desc="Загрузка фото на Яндекс Диск"):
                        await future

                    print("Загрузка всех фотографий на Яндекс Диск завершена.")
                else:
                    print(f"В папке '{photos_dir}' нет фотографий для загрузки на Яндекс Диск.")
            else:
                print(f"Папка '{photos_dir}' не найдена.")
        else:
            print(f"Не удалось создать папку '{disk_folder}' на Яндекс Диске. Загрузка отменена.")
