import os
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = os.getenv('SESSION_NAME')
client_id_ya = os.getenv('CLIENT_ID_YA')
client_secret_ya = os.getenv('CLIENT_SECRET_YA')
auth_code = os.getenv('AUTH_CODE')
ya_disk_token = os.getenv('YA_DISK_TOKEN')
