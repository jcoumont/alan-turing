
from src.reminders.messages import Message, Messages, Card

messages: Messages = (
        f"c'est l'heure de la **pause** ! On se revoit dans %s minutes",
        f"une pause de plus, quelle chance ! On se revoit dans %s minutes"
)


class PauseMessage(Message):

    def __init__(self, duration: int) -> None:
        """
        Pause message: used in a reminder that need to reminds to take a break.

        :param duration: The duration of the pause
        """

        self.duration = duration
        Message.__init__(self, messages)

    def get_content(self):

        # Append the event variables (name, delay) to the message
        message = super().get_content()[0]
        return message % self.duration, self.card
