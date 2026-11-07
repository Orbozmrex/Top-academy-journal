ITTop-Journal-SDK
---

A modern, easy to use, async API wrapper for top academy journal written in Python. 

[journal.top-academy.ru](https://journal.top-academy.ru)

Installation
---
```bash
python3 -m pip install -U aaaaaaa
```

Quick example
---
```python
import asyncio
from top_academy_journal import Journal, HomeworkStatus
from datetime import datetime, timedelta

async def main():
    async with Journal("login", "password") as j:
        homework = await j.fetch_homework(HomeworkStatus.EXPIRED)
        print(homework)

        today = datetime.today()
        schedule = await j.fetch_schedule(start_date=today, end_date=today + timedelta(days=7))
        print(schedule)
    
asyncio.run(main())
```

Journal methods
---

<details>
  <summary>👤 User Information</summary>

  - **`fetch_userinfo()`** -> `UserInfo`  
    Fetches user profile data directly from the API.
  - **`get_userinfo()`** -> `UserInfo | None`  
    Returns user profile data from the local cache.
</details>

<details>
  <summary>📚 Homework</summary>

  - **`fetch_homework(status: HomeworkStatus, homework_type: HomeworkType, subject_id: int)`** -> `List[Homework]`
    Fetches a list of homework filtered by status, type, and subject id.
  - **`get_homework(id: int)`** -> `Homework | None`  
    Retrieves homework from the cache.
  - **`upload_homework(homework: Homework, file_path: str, spent_hour: int, spent_min: int, comment: str)`** -> `HomeworkStudent`  
    Uploads or re-uploads a completed homework.
</details>

<details>
  <summary>📅 Schedule & Attendance</summary>

  - **`fetch_schedule(start_date: datetime, end_date: datetime)`**  
    Fetches schedule for a specific date range directly from the API.
  - **`fetch_student_visits(subject_id: int)`**  
    Fetches student's attendance records and grades.
</details>

<details>
  <summary>👥 Group Specs</summary>

  - **`fetch_group_specs()`** -> `List[SubjectInfo]`  
    Fetches group subjects directly from the API.
  - **`get_group_specs(id: int)`** -> `SubjectInfo | dict[int, SubjectInfo]`  
    Retrieves group subjects from the cache.
</details>