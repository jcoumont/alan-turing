
from src.reminders.messages import Message,  Card

# my.becode.org URL
URL = "https://my.becode.org"


class AttendanceMessage(Message):

    card = Card(
        title="MyBecode.org",
        url=URL,
        description=f"In Attendance We Trust ! Pointez maintenant sur [my.becode.org]({URL}).",
        color=5747135,
        thumbnail="https://i.imgur.com/cg4xd66.png"
    )

    message = f"c'est le moment de pointer sur {URL}"

    def __init__(self) -> None:
        """
        Attendance message: used in a reminder that need to reminds to go to my.becode.org
        """
        self.name = "attendance"
        super().__init__(AttendanceMessage.message, URL)

    @staticmethod
    def get_card() -> Card:
        return AttendanceMessage.card
