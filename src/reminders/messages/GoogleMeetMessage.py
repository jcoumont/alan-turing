
from src.reminders.messages import Message, Messages, Card

# Google meet URL
URL = "https://meet.google.com/hfe-twue-vsb"

# Google Meet card
card = Card(
    title="Google Meet",
    url=URL,
    description=f"Votre coach préféré vous invite à participer à la [visioconférence]({URL}) des Turings sur Google Meet.",
    color=3510917,
    thumbnail={"url": "https://i.imgur.com/ehlNUYU.png"}
)

# Google Meet messages
messages: Messages = (
    f"%s démarre dans **%s minutes** sur [Google Meet]({URL})",
    f"%s dans **%s minutes** sur [Google Meet]({URL})"
)


class GoogleMeetMessage(Message):

    def __init__(self, event_name: str, delay: int) -> None:
        """
        Google Meet message: used in a reminder that need to reminds to go to Google Meet.

        :param event_name: The name of the Google Meet event.
        :param delay: Delay (in minutes) until the starting of this event.
        """

        self.event_name = event_name
        self.delay = delay

        super().__init__(messages, card, URL)

    def get_content(self):
        """Override Message.get_content to insert the event_name and the delay."""

        # Append the event variables (name, delay) to the message
        message = super().get_content()[0]
        return message % (self.event_name, self.delay), self.card
