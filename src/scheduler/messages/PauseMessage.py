from src.scheduler.messages import Message, MessageWeight


class PauseMessage(Message):

    message = f"c'est l'heure de la **pause** ! On se revoit dans **%s minutes**"

    def __init__(self, duration: int) -> None:
        """
        Pause message: used in a reminder that need to reminds to take a break.

        :param duration: The duration of the pause
        """
        super().__init__(PauseMessage.message)

        self.weight = MessageWeight.PAUSE
        self.duration = duration

    def get_message(self) -> str:

        # Append the event variables (name, delay) to the message
        return self.message % self.duration
