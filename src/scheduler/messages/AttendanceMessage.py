import copy
from typing import Tuple
from src.scheduler.messages import Message, Card, MessageWeight
from src.web.becode import Periods, Locations

# my.becode.org URL
URL = "https://my.becode.org"


class AttendanceMessage(Message):

    card = Card(
        title="My Becode",
        url=URL,
        description=f"In Attendance We Trust ! Pointez maintenant sur [my.becode.org]({URL}). Ou cliquez directement sur la réaction ci-dessous.",
        color=5747135,
        thumbnail="https://i.imgur.com/ixU2HdV.gif",  # "https://i.imgur.com/cg4xd66.png",
        footer="Vous pointerez pour %s @ %s.",
    )

    message = f"c'est le moment de pointer sur {URL}"

    def __init__(self, period: Periods, at_home: Locations) -> None:
        """
        Attendance message: used in a reminder that need to reminds to go to my.becode.org
        """
        super().__init__(AttendanceMessage.message, URL)

        self.weight = MessageWeight.ATTENDANCE

        self.period = period
        self.at_home = at_home

    def get_card(self) -> Card:

        card = copy.copy(AttendanceMessage.card)
        card.footer = card.footer % (self.period.value, self.at_home.value[0])

        return card

    def get_attendance_details(self) -> Tuple[Periods, Locations]:
        return self.period, self.at_home
