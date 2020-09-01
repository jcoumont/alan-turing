
from typing import NamedTuple, Tuple, Dict
import random

Messages = Tuple[str, ...]


class Card(NamedTuple):
    title: str
    url: str
    description: str
    color: int
    thumbnail: Dict


class Message:

    def __init__(self, messages: Messages, card: Card = None, url: str = None) -> None:

        self.messages = messages
        self.card = card
        self.url = url

    def get_content(self) -> Tuple[str, Card]:
        """Return a tuple with a message and the card."""

        return self.__get_random_message(), self.card

    def __get_random_message(self) -> str:
        """Retrieve and return randomly a message from self.messages."""

        return random.choice(self.messages)
