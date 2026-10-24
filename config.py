import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    headers: dict = {"Referer": "https://journal.top-academy.ru/", 
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    _username: str = os.getenv("LOGIN")
    _password: str = os.getenv("PASSWORD")
    _app_key: str = os.getenv("APPLICATION_KEY")

settings: Settings = Settings()