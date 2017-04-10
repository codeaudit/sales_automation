import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# GLOBAL VARIABLES
APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")
TOKEN = os.environ.get("TOKEN")
DB = os.environ.get("DB_NAME")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")