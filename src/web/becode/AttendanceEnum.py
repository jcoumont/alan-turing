
from enum import Enum


# Sources: https://github.com/becodeorg/graph/blob/develop/src/schema/models/attendances/types/attendance-time-period.js
class Periods(Enum):

    MORNING = "09h00"
    LUNCH = "12h30"
    NOON = "13h30"
    EVENING = "17h00"


class Locations(Enum):

    HOME = ("Home", True)  # at_home = True
    BECODE = ("Becode", False)  # at_home = False
