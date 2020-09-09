
from enum import Enum


# Sources: https://github.com/becodeorg/graph/blob/develop/src/schema/models/attendances/types/attendance-time-period.js
class TimePeriodsEnum(Enum):

    MORNING = "MORNING",
    LUNCH = "LUNCH",
    NOON = "NOON",
    EVENING = "EVENING"
