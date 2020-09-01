
from src.reminders.messages import Message, Messages, Card

messages: Messages = (
        f"c'est l'heure de la **pause** ! On se revoit dans %s minutes",
        f"une pause de plus, quelle chance ! On se revoit dans %s minutes"
)


class PauseMessage(Message):

    def __init__(self, delay: int) -> None:
        self.delay = delay
        Message.__init__(self, messages)

    def get_content(self):

        # Append the event variables (name, delay) to the message
        message = super().get_content()[0]
        return message % self.delay, self.card
