from enum import IntEnum

class HomeworkStatus(IntEnum):
    EXPIRED = 0
    REVIEWED = 1
    ONREVIEW = 2
    UNDONE = 3
    EDITED = 4 #no clue what this status means
    DELETED = 5

class Gender(IntEnum):
    MALE = 0
    FEMALE = 1

class HomeworkType(IntEnum):
    HOMEWORK = 0
    LABORATORY = 1