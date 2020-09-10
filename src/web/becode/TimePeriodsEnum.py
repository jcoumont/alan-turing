
from enum import Enum


# Sources: https://github.com/becodeorg/graph/blob/develop/src/schema/models/attendances/types/attendance-time-period.js
class TimePeriodsEnum(Enum):

    MORNING = "09h00",
    LUNCH = "12h30",
    NOON = "13h30",
    EVENING = "17h00"
