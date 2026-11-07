import httpx
from top_academy_journal.endpoints import endpoints
from top_academy_journal.enums import HomeworkStatus, HomeworkType
from top_academy_journal.models.homework import Homework, HomeworkStudent
from top_academy_journal.models.schedule import ScheduleLesson, LessonVisit, SubjectInfo
from top_academy_journal.models.student import UserInfo
from typing import List
from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode
import re

class Journal:
    def __init__(self, username: str, password: str):
        self._client = httpx.AsyncClient(base_url="https://msapi.top-academy.ru/api/v2", 
                                         headers={"Referer": "https://journal.top-academy.ru/"},
                                         timeout=30,
                                         transport=httpx.AsyncHTTPTransport(retries=3))
        self._username: str = username
        self._password: str = password
        self._app_key: str | None = None
        self._is_authorized: bool = False
        self._user_info: UserInfo | None = None
        self._homework: dict[int, Homework] = {}
        self._group_specs: dict[int, SubjectInfo] = {} 

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def _refresh_app_key(self):
        with httpx.Client(base_url="https://journal.top-academy.ru") as client:
            try:
                response = client.get("/auth/login/")
                match = re.search(r'src="(/app\.[^"]+\.js)"', response.text)

                app_url = match.group(1)

                js_content = client.get(app_url)
                match = re.search(r'AuthModel\("([^"]+)"\)', js_content.text)
                
                app_key = match.group(1)
                self._app_key = app_key
            except AttributeError:
                print("Unable to find application key")

    async def _auth(self):
        if self._app_key is None:
            await self._refresh_app_key()

        response = await self._client.post(endpoints["login"], json={"username": self._username, "password": self._password, "application_key": self._app_key})
        access_token = response.json()
        self._client.headers.update({"Authorization": f"Bearer {access_token["access_token"]}"})
        self._is_authorized = True

    async def _request(self, method: str, url: str, **kwargs):
        max_retries = 2
        for attempt in range(max_retries):
            if not self._is_authorized:
                await self._auth()
                
            response = await self._client.request(method, url, **kwargs)
            if response.status_code == 401:
                self._is_authorized = False
                continue
            
            if response.status_code != 410 or attempt == max_retries - 1:
                return response
                
            self._is_authorized = False 
            await self._refresh_app_key()

    async def fetch_userinfo(self) -> UserInfo:
        response = await self._request("GET", endpoints["userinfo"])
        user_info = UserInfo.model_validate(response.json())

        self._user_info = user_info
        return user_info

    def get_userinfo(self) -> UserInfo:
        return self._user_info

    async def fetch_homework(self, status: HomeworkStatus | None = None, homework_type: HomeworkType | None = None, subject_id: int | None = None) -> List[Homework]:
        params = {}
        if status is not None:
            params["status"] = status
        if homework_type is not None:
            params["type"] = homework_type
        if subject_id is not None:
            params["subject_id"] = subject_id

        base_url = endpoints["homework"]
        if params:
            url = f"{base_url}?{urlencode(params)}"
        else:
            url = base_url

        response = await self._request("GET", url)
        response_json = response.json()
        homework_list = [Homework.model_validate(hw) for hw in response_json]

        for hw in homework_list:
            self._homework[hw.id] = hw
        return homework_list

    def get_homework(self, id: int | None = None) -> Homework | dict[int, Homework]:
        return self._homework.get(id) if id is not None else self._homework

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

    async def fetch_schedule(self, start_date: datetime, end_date: datetime | None = None):
        start_date = start_date.strftime("%Y-%m-%d")
        url = f"{endpoints["schedule"]}{start_date}"
        if end_date is not None:
            end_date = end_date.strftime("%Y-%m-%d")
            url += f"&date_end={end_date}"

        response = await self._request("GET", url)
        response_json = response.json()
        return [ScheduleLesson.model_validate(lesson) for lesson in response_json]

    async def fetch_student_visits(self, subject_id: int | None = None):
        url = endpoints["visits"]
        if subject_id is not None:
            url += f"?subject_id={subject_id}"

        response = await self._request("GET", url)
        response_json = response.json()
        return [LessonVisit.model_validate(visit) for visit in response_json]

    async def fetch_group_specs(self) -> List[SubjectInfo]:
        response = await self._request("GET", endpoints["group_specs"])
        response_json = response.json()

        specs = [SubjectInfo.model_validate(spec) for spec in response_json]
        for spec in specs:
            self._group_specs[spec.id] = spec
        return specs 

    def get_group_specs(self, id: int | None = None) -> SubjectInfo | dict[int, SubjectInfo]:
        return self._group_specs if id is None else self._group_specs.get(id)

    async def aclose(self) -> None:
        await self._client.aclose()