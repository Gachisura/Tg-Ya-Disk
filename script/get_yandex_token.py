import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id_ya = os.getenv('CLIENT_ID_YA')
client_secret_ya = os.getenv('CLIENT_SECRET_YA')
auth_code = os.getenv('AUTH_CODE')


def get_oauth_token(client_id_ya, client_secret_ya, auth_code):
    """Получает OAuth-токен Яндекс Диска (обычно запускается один раз для получения YA_DISK_TOKEN)."""
    url = 'https://oauth.yandex.ru/token'
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': client_id_ya,
        'client_secret': client_secret_ya
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get('access_token'), token_data.get('refresh_token')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении OAuth-токена: {e}")
        if response is not None:
            print(f"Код ответа: {response.status_code}")
            print(f"Тело ответа: {response.text}")
        return None, None
