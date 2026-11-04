from pydantic import BaseModel, Field, AnyHttpUrl
from datetime import datetime
from ..enums import HomeworkStatus

class HomeworkStudent(BaseModel):
    id: int
    created_at: datetime = Field(alias='creation_time')
    file_path: AnyHttpUrl | None
    mark: int | None
    comment: str | None = Field(alias='stud_answer')

class Homework(BaseModel):
    id: int
    subject: str = Field(alias='name_spec')
    subject_id: int
    theme: str | None
    comment: str | None
    deadline_time: datetime = Field(alias='completion_time')
    creation_time: datetime
    preview_image: AnyHttpUrl | None = Field(alias='cover_image')
    file_path: AnyHttpUrl | None
    teacher_name: str = Field(alias='fio_teach')
    teacher_id: int = Field(alias='id_teach')
    status: HomeworkStatus
    homework_student: HomeworkStudent | None = Field(alias='homework_stud')