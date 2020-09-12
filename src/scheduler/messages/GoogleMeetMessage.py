
from src.scheduler.messages import Message, Card, MessageWeight

# Google meet URL
URL = "https://meet.google.com/hfe-twue-vsb"


class GoogleMeetMessage(Message):

    card = Card(
        title="Google Meet",
        url=URL,
        description=f"Votre coach préféré vous invite à participer à la [visioconférence]({URL}) des Turings sur Google Meet.",
        color=3510917,
        thumbnail="https://i.imgur.com/ehlNUYU.png"
    )

    message = f"%s démarre dans **%s minutes** sur **Google Meet**"

    def __init__(self, event_name: str, delay: int) -> None:
        """
        Google Meet message: used in a reminder that need to reminds to go to Google Meet.

        :param event_name: The name of the Google Meet event.
        :param delay: Delay (in minutes) until the beginning of this event.
        """
        super().__init__(GoogleMeetMessage.message, URL)

        self.weight = MessageWeight.MEET

        self.event_name = event_name
        self.delay = delay

    def get_message(self) -> str:
        """Override Message.get_content to insert the event_name and the delay."""

        # Append the event variables (name, delay) to the message
        return self.message % (self.event_name, self.delay)

    @staticmethod
    def get_card() -> Card:
        return GoogleMeetMessage.card
