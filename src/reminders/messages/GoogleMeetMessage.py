
from src.reminders.messages import Message, Messages, Card

URL = "https://my.becode.org/dashboard"

card = Card(
        title="Google Meet",
        url=URL,
        description=f"Participez à la [visioconférence]({URL}) des Turings "
                    f"sur Google Meet.",
        color=3510917,
        thumbnail={"url": "https://i.imgur.com/ehlNUYU.png"}
)

messages: Messages = (
        f"la %s démarre dans %s minutes sur [Google Meet]({URL})",
        f"%s dans %s minutes sur [Google Meet]({URL})"
)


class GoogleMeetMessage(Message):

    def __init__(self, event_name: str, delay: int) -> None:
        self.event_name = event_name
        self.delay = delay

        super().__init__(messages, card, URL)

    def get_content(self):

        # Append the event variables (name, delay) to the message
        message = super().get_content()[0]
        return message % (self.event_name, self.delay), self.card
