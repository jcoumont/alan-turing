
from typing import Tuple
from src.reminders.messages import Message,  Card
from src.web.becode import TimePeriodsEnum

# my.becode.org URL
URL = "https://my.becode.org"


class AttendanceMessage(Message):

    card = Card(
        title="MyBecode.org",
        url=URL,
        description=f"In Attendance We Trust ! Pointez maintenant sur [my.becode.org]({URL}). Ou cliquez directement sur la réaction ci-dessous !",
        color=5747135,
        thumbnail="https://i.imgur.com/cg4xd66.png"
    )

    message = f"c'est le moment de pointer sur {URL}"

    def __init__(self, period: TimePeriodsEnum, at_home: bool) -> None:
        """
        Attendance message: used in a reminder that need to reminds to go to my.becode.org
        """
        self.name = "attendance"

        self.period = period
        self.at_home = at_home

        super().__init__(AttendanceMessage.message, URL)

    @staticmethod
    def get_card() -> Card:
        return AttendanceMessage.card

    def get_attendance_details(self) -> Tuple[TimePeriodsEnum, bool]:
        return self.period, self.at_home
