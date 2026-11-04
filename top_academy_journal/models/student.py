from pydantic import BaseModel, Field
from datetime import datetime
from ..enums import Gender

class UserInfo(BaseModel):
    id: int = Field(alias='student_id')
    name: str = Field(alias='full_name')
    gender: Gender
    birthday: datetime
    age: int
    group_id: int = Field(alias='current_group_id')
    group_name: str
    last_visit: datetime = Field(alias='last_date_visit')
    registered_at: datetime = Field(alias='registration_date')
    study_form: str = Field(alias='study_form_short_name')
    visibility: dict
    gaming_points: list