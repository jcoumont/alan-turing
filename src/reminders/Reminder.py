
from src.web import WebRequest
import random
from pytz import timezone
from typing import NamedTuple, Tuple
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


# Initialize the scheduler and setup the timezone.
scheduler = BlockingScheduler()
tz = timezone('Europe/Amsterdam')


class Link(NamedTuple):
    """
    Link data structure. A "link" is a bunch of text to place between
    two sentences to "link" them.
    """

    message: str
    needPoint: bool  # True if the previous sentence need a point.
    needUppercase: bool  # True if the following sentence need an uppercase.


# List of linkers (text that link two sentences together)
linkers: Tuple = (
    Link(message="", needPoint=True, needUppercase=True),
    Link(message=". Et", needPoint=False, needUppercase=False)
)


class Reminder:

    def __init__(self, name: str, days: str, hour: int, minute: int, sources: list):
        """
        Core of this Bot: Create a scheduled element that will send a POST request
        to the Discord webhook.

        :param name: The name of the reminder. For clarity only.
        :param days: Days of the week when this reminder has to trigger.
        :param hour: Hour of the day when this reminder has to trigger.
        :param minute: Minutes of when this reminder has to trigger.
        :param sources: List of Message object containing the text and card used to generate a Reminder.
        """
        self.sources = self.get_message_card_from_source(sources)
        self.message, self.card = self.format_message_card()

        self.__initialize(name, days, hour, minute)

    @staticmethod
    def get_linker() -> Link:
        """Return a randomly chooser text to link to tenses."""

        return random.choice(linkers)

    @staticmethod
    def get_message_card_from_source(sources: list) -> list:
        """
        Retrieve messages and cards from the source and return a raw version.

        :return: return Raw iterator of messages anc cards to show.
        """

        return list(zip(entry.get_content() for entry in sources))

    def format_message_card(self) -> Tuple[str, tuple]:
        """
        Create an sanitize a message and a card to be send to the webhook.

        :return: Tuple (message: str, Card)
        """

        # Retrieve the linker and the first message.
        linker: Link = self.get_linker()
        messages = [self.format_uppercase(self.sources[0][0][0])]

        # If there's more than one message:
        if len(self.sources) > 1:

            # Format the end of the first message.
            if linker.needPoint:
                messages[0] = self.format_end_tense(messages[0])

            # Retrieve the second message.
            messages.append(self.format_end_tense(self.sources[1][0][0]))

            # Format the beginning of the second message.
            if linker.needUppercase:
                messages[1] = self.format_uppercase(messages[1])

            # Append the linker
            messages.insert(1, linker.message)

        return "".join(messages), self.sources[0][0][1]

    @staticmethod
    def format_uppercase(text: str) -> str:
        """
        Transform the first letter of a given string to uppercase.
        Return the result.
        """

        return "".join([text[0].capitalize(), text[1:]])

    @staticmethod
    def format_end_tense(text: str) -> str:
        """
        Add punctuation to the end of a tense.

        :param text: The text to transform.
        :return: The modified text
        """

        return f"{text}."

    def __initialize(self, name: str, days: str, hour: int, minute: int) -> None:
        """
        The core of the Reminder class: This function create a scheduler to
        post self.message and self.card on Discord via a WebRequest.

        Used internally only. Parameters are the same than this class.
        """

        @scheduler.scheduled_job('cron', day_of_week=days, hour=hour, minute=minute, timezone=tz)
        def job():

            # Job triggered
            print(f"[!] Job triggered: {datetime.now()} - {name}.")
            WebRequest(self.message, self.card).send()

        # Job registered
        print(f"[+] Job scheduled: {days} @ {hour}h{minute} - {name}.")

    @staticmethod
    def start():
        """Start all schedulers."""
        scheduler.start()
