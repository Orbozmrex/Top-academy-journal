from pydantic import BaseModel, Field, model_validator
from datetime import datetime, time

class ScheduleLesson(BaseModel):
    date: datetime
    starts_at: time = Field(alias='started_at')
    ends_at: time = Field(alias='finished_at')
    teacher_name: str
    subject_name: str
    room_name: str

class LessonVisit(BaseModel):
    date: datetime = Field(alias='date_visit')
    subject_id: int
    lesson_theme: str
    teacher_name: str
    subject_name: str = Field(alias='spec_name')
    marks: dict = {}

    @model_validator(mode="before")
    @classmethod
    def get_marks(cls, data: dict) -> dict:
        data["marks"] = {key: value for key, value in data.items() if key.endswith("_mark") and value is not None}
        return data

class SubjectInfo(BaseModel):
    id: int
    name: str
    short_name: str