import httpx
from top_academy_journal.endpoints import endpoints
from top_academy_journal.enums import HomeworkStatus
from top_academy_journal.models import Homework, UserInfo, HomeworkStudent
from typing import List
from pathlib import Path

class Journal:
    def __init__(self, username: str, password: str):
        self._client = httpx.AsyncClient(base_url="https://msapi.top-academy.ru/api/v2", 
                                         headers={"Referer": "https://journal.top-academy.ru/", 
                                                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
                                         timeout=30)
        self._username: str = username
        self._password: str = password
        self._app_key: str = "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6"
        self._is_authorized: bool = False
        self._user_info: UserInfo | None = None
        self._homework: dict[int, Homework] = {}

    async def _auth(self):
        response = await self._client.post(endpoints["login"], json={"username": self._username, "password": self._password, "application_key": self._app_key})
        access_token = response.json()
        self._client.headers.update({"Authorization": f"Bearer {access_token["access_token"]}"})
        self._is_authorized = True

    async def _request(self, method: str, url: str, **kwargs):
        if not self._is_authorized:
            await self._auth()

        return await self._client.request(method, url, **kwargs)

    async def fetch_userinfo(self) -> UserInfo:
        response = await self._request("GET", endpoints["userinfo"])
        user_info = UserInfo.model_validate(response.json())

        self._user_info = user_info
        return user_info

    def get_userinfo(self) -> UserInfo:
        return self._user_info

    async def fetch_homework(self, status: HomeworkStatus = HomeworkStatus.UNDONE) -> List[Homework]:
        response = await self._request("GET", f"{endpoints["homework"]}{status}")
        response_json = response.json()
        homework_list = [Homework.model_validate(hw) for hw in response_json]

        for hw in homework_list:
            self._homework[hw.id] = hw
        return homework_list

    def get_homework(self, id: int) -> Homework:
        return self._homework.get(id)

    async def upload_homework(self, homework: Homework, file_path: str, spent_hour: int = 0, spent_min: int = 30, comment: str = '') -> HomeworkStudent:
        if not (0 <= spent_hour <= 99):
            raise ValueError("spent_hour must be between 0 and 99")

        if not (0 <= spent_min <= 59):
            raise ValueError("spent_min must be between 0 and 59")
    
        if homework.homework_student is not None:
            await self._request("POST", endpoints["homework_delete"], json={"id": homework.homework_student.id})

        data = {
            "id": homework.id,
            "answerText": comment,
            "spentTimeHour": f"{spent_hour:02d}",
            "spentTimeMin": f"{spent_min:02d}"
        }
        
        path = Path(file_path).resolve()
        file_name = path.name
        with open(path, "rb") as file:
            files = {"file": (file_name, file)}
            response = await self._request("POST", endpoints["homework_upload"], data=data, files=files)
            return HomeworkStudent.model_validate(response.json())