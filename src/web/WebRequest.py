
import requests
from os import environ
from typing import NamedTuple

# Load environment variables
URL = environ.get('WEBHOOK')


class WebRequest:

    properties = {
        "username": "Alan Turing",
        "avatar_url": "https://i.imgur.com/JD51N3v.jpg"
    }

    def __init__(self, content: str = None, card=None):
        """
        Send a web request to Discord with the given content and card.
        :param content:
        :param card:
        """
        self.json = self.__create_json(content, card)

    @staticmethod
    def __create_json(content, card: NamedTuple):

        if card is not None:
            WebRequest.properties["embeds"] = [card._asdict()]

        if content is not None:
            WebRequest.properties["content"] = content

        return WebRequest.properties

    def send(self):
        requests.post(URL, json=self.json)
