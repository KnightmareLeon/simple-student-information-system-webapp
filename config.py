import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "localhost")
USER = os.getenv("DB_USER", "postgres")
DATABASE = os.getenv("DATABASE", "makeyourowndb")
PASSWORD = os.getenv("PASSWORD", "trololololololol")
PORT = os.getenv("PORT", "5432")
SECRET_KEY = os.getenv("SECRET_KEY", "keysosecretnooneknow")
DEBUG = os.getenv("FLASK_DEBUG")