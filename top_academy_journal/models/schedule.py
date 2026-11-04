from pydantic import BaseModel, Field
from datetime import datetime, time

class ScheduleLesson(BaseModel):
    date: datetime
    starts_at: time = Field(alias='started_at')
    ends_at: time = Field(alias='finished_at')
    teacher_name: str
    subject_name: str
    room_name: str