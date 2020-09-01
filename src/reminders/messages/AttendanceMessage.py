
from src.reminders.messages import Message, Messages, Card

URL = "https://my.becode.org/dashboard"

card = Card(
        title="MyBecode.org",
        url=URL,
        description="Pointez sur my.becode.org !",
        color=5747135,
        thumbnail={"url": "https://i.imgur.com/cg4xd66.png"}
)

messages: Messages = (
        f"pensez à [pointer]({URL})",
        f"n'oubliez pas de [pointer]({URL})"
)


class AttendanceMessage(Message):

    def __init__(self) -> None:
        Message.__init__(self, messages, card, URL)
