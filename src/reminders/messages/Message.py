
from typing import NamedTuple, Tuple, Dict
import random

Messages = Tuple[str, ...]


class Card(NamedTuple):
    """Card data structure. Used to store card details."""

    title: str
    url: str
    description: str
    color: int
    thumbnail: Dict


class Message:

    def __init__(self, messages: Messages, card: Card = None, url: str = None) -> None:
        """
        Message class: Generate a message and a card to be used in a Reminder.

        :param messages: A tuple of messages which will be used to return one single message.
        :param card: Optional: A Card object containing a card's data.
        :param url: Optional: An URL to be included in the card.
        """

        self.messages = messages
        self.card = card
        self.url = url

    def get_content(self) -> Tuple[str, Card]:
        """Return a tuple with a randomly chosen message and the card."""

        return self.__get_random_message(), self.card

    def __get_random_message(self) -> str:
        """Retrieve and return randomly a message from self.messages."""

        return random.choice(self.messages)
