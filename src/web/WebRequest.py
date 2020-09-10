
from src import config

import requests
from os import environ
from typing import NamedTuple


class WebRequest:

    properties = {
        "username": "Alan Turing",
        "avatar_url": "https://i.imgur.com/JD51N3v.jpg"
    }

    def __init__(self, content: str = None, card=None):
        """
        Initialize a web request to Discord with the given content and card.

        :param content: The text to send as a message.
        :param card: The embedded card to send with the message.
        """
        self.json = self.__create_json(content, card)

    @staticmethod
    def __create_json(content: str, card: NamedTuple):
        """
        Create a json filled with all properties and data to send to Discord.

        :param content: The text to send as a message.
        :param card: The embedded card to send with the message.
        :return: The data and properties, in a dictionary.
        """

        # If a card is given, append it to the properties
        if card is not None:
            WebRequest.properties["embeds"] = [card._asdict()]

        # If a message is given, append it to the properties
        if content is not None:
            WebRequest.properties["content"] = content

        return WebRequest.properties

    def send(self):
        """Execute the request."""

        requests.post(config.WEBHOOK, json=self.json)
