from enum import IntEnum

class HomeworkStatus(IntEnum):
    EXPIRED = 0
    REVIEWED = 1
    ONREVIEW = 2
    UNDONE = 3

class Gender(IntEnum):
    MALE = 0
    FEMALE = 1