import os

from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.getenv('TOKEN')
DB_URL = os.getenv('DB_URL')

ADMINS = [2039584148]