
from src.reminders.messages import Message, Messages, Card

# my.becode.org URL
URL = "https://my.becode.org/dashboard"

# Attendance card
card = Card(
    title="MyBecode.org",
    url=URL,
    description=f"In Attendance We Trust ! Pointez maintenant sur [my.becode.org]({URL}).",
    color=5747135,
    thumbnail={"url": "https://i.imgur.com/cg4xd66.png"}
)

# Attendance messages
messages: Messages = (
    f"pensez à [pointer]({URL})",
    f"n'oubliez pas de [pointer]({URL})",
    f"le dernier à pointer sur [becode]({URL}) a perdu"
)


class AttendanceMessage(Message):

    def __init__(self) -> None:
        """
        Attendance message: used in a reminder that need to reminds to go to my.becode.org
        """

        Message.__init__(self, messages, card, URL)
