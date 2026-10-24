import httpx
from top_academy_journal.endpoints import endpoints
from top_academy_journal.enums import HomeworkStatus

class Journal:
    def __init__(self, username: str, password: str):
        self._client = httpx.AsyncClient(base_url="https://msapi.top-academy.ru/api/v2", 
                                         headers={"Referer": "https://journal.top-academy.ru/", 
                                                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
                                         timeout=30)
        self._username = username
        self._password = password
        self._app_key = "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6"
        self.is_authorized = False

    async def _auth(self):
        response = await self._client.post(endpoints["login"], json={"username": self._username, "password": self._password, "application_key": self._app_key})
        access_token = response.json()
        self._client.headers.update({"Authorization": f"Bearer {access_token["access_token"]}"})
        self.is_authorized = True

    async def _request(self, method: str, url: str, **kwargs):
        if not self.is_authorized:
            await self._auth()

        return await self._client.request(method, url, **kwargs)

    async def get_user_info(self):
        response = await self._request("GET", endpoints["userinfo"])
        return response.json()

    async def get_homework(self, status: HomeworkStatus = HomeworkStatus.UNDONE):
        response = await self._request("GET", f"{endpoints["homework"]}{status}")
        return response.json()