import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DB_URL')
db_name = os.getenv('DB_NAME')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
app_name = os.getenv('APP_NAME')
