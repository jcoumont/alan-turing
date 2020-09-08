
from typing import NamedTuple, Dict


class Card(NamedTuple):
    """Card data structure. Used to store card details."""

    title: str
    url: str
    description: str
    color: int
    thumbnail: str


class Message:

    def __init__(self, message: str, url: str = None) -> None:
        """
        Message class: Generate a message and a card to be used in a Reminder.

        :param message: A tuple of messages which will be used to return one single message.
        :param url: Optional: An URL to be included in the card.
        """

        self.message = message
        self.url = url

    def get_message(self) -> str:
        """Return a tuple with a randomly chosen message and the card."""

        return self.message

    @staticmethod
    def get_card() -> None:
        return None
