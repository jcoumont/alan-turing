from dataclasses import dataclass
from discord import Embed
from enum import Enum


@dataclass
class Card:
    """Card data structure. Used to store card details."""

    title: str
    url: str
    description: str
    color: int
    thumbnail: str
    footer: str = None

    def get_embed(self):

        embed = Embed(
            title=self.title,
            description=self.description,
            url=self.url,
            colour=self.color,
        )
        embed.set_thumbnail(url=self.thumbnail)

        if self.footer:
            embed.set_footer(text=self.footer)

        return embed


class Message:
    def __init__(self, message: str, url: str = None) -> None:
        """
        Message class: Generate a message and a card to be used in a Reminder.

        :param message: A tuple of messages which will be used to return one single message.
        :param url: Optional: An URL to be included in the card.
        """

        self.message = message
        self.url = url

        self.weight = MessageWeight.TEXT

    def get_message(self) -> str:
        """Return a tuple with a randomly chosen message and the card."""

        return self.message

    @staticmethod
    def get_card() -> None:
        return None


class MessageWeight(Enum):
    """Enum message type by importance. Smaller value = More important !"""

    ATTENDANCE = 0
    MEET = 2
    PAUSE = 3
    TEXT = 4
