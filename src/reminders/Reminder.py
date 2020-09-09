
from src import globals

import time
import random
from discord import Embed, Message
from src.storage import Database
from pytz import timezone
from typing import NamedTuple, Tuple, List
from src.reminders.messages import Message
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot
from os import environ

CHANNEL_ID = int(environ.get('DISCORD_CHANNEL'))


# Initialize the scheduler and setup the timezone.
scheduler = AsyncIOScheduler()
tz = timezone('Europe/Brussels')


class Link(NamedTuple):
    """
    A "Link" is a bunch of text to place between
    two sentences to "link" them.
    """

    message: str
    needPoint: bool  # True if the previous sentence need a point.
    needUppercase: bool  # True if the following sentence need an uppercase.


# List of linkers (text that link two sentences together)
linkers: Tuple = (
    Link(message="", needPoint=True, needUppercase=True),
    Link(message=". Et ", needPoint=False, needUppercase=False)
)


class Reminder:

    def __init__(self, client: Bot, name: str, days: str, hour: int, minute: int, mentions: bool, messages: List[Message]):
        """
        Core of this Bot: Create a scheduled element that will send a POST request
        to the Discord webhook.

        :param name: The name of the reminder. For clarity only.
        :param days: Days of the week when this reminder has to trigger.
        :param hour: Hour of the day when this reminder has to trigger.
        :param minute: Minutes of when this reminder has to trigger.
        :param mentions: True if this reminder has to mentions the members.
        :param messages: List of Message object containing the text and card used to generate a Reminder.
        """
        self.db = Database()
        self.client = client
        self.mentions = mentions

        self.attendance = False
        self.message = self.format_message(self.retrieve_messages(messages))
        self.card = self.create_card(self.retrieve_raw_card(messages))

        self.__initialize(name, days, hour, minute)

    @staticmethod
    def get_linker() -> Link:
        """Return a randomly chooser text to link to tenses."""

        return random.choice(linkers)

    @staticmethod
    def retrieve_messages(messages):
        """Retrieve and return the messages text from the given message object."""
        message_list = []

        for message in messages:
            message_list.append(message.get_message())

        return message_list

    def retrieve_raw_card(self, messages):
        """Retrieve and return the card from the messages."""
        meet = False

        for message in messages:
            if message.name == "attendance":
                self.attendance = True

            if message.name == "googlemeet":
                meet = message.get_card()

        if meet:
            return meet

        return messages[0].get_card()

    @staticmethod
    def create_card(card):

        if card:

            embed = Embed(
                title=card.title,
                description=card.description,
                url=card.url,
                colour=card.color
            )
            embed.set_thumbnail(url=card.thumbnail)

            return embed
        return None

    def format_message(self, raw_text: list) -> str:
        """
        Create an sanitize a message and a card to be send to the webhook.

        :return: Tuple (message: str, Card)
        """
        messages = []

        # Retrieve the linker and the first message.
        linker: Link = self.get_linker()
        messages.append(self.to_uppercase(raw_text[0]))

        # If there's more than one message:
        if len(raw_text) > 1:

            # Format the end of the first message.
            if linker.needPoint:
                raw_text[0] = self.add_point(raw_text[0])

            # Retrieve the second message.
            messages.append(self.add_point(raw_text[1]))

            # Format the beginning of the second message.
            if linker.needUppercase:
                messages[1] = self.to_uppercase(messages[1])

            # Append the linker
            messages.insert(1, linker.message)

        return "".join(messages)

    @staticmethod
    def to_uppercase(text: str) -> str:
        """
        Transform the first letter of a given string to uppercase.
        Return the result.
        """

        return "".join([text[0].capitalize(), text[1:]])

    @staticmethod
    def add_point(text: str) -> str:
        """
        Add punctuation to the end of a tense.

        :param text: The text to transform.
        :return: The modified text
        """

        return f"{text}."

    def add_mentions(self, text: str) -> str:
        users = self.db.get_users_to_mention()

        # Set users to empty string if the list is empty
        if len(users) == 0:
            users = ""

        # Append the users to mention
        return "".join([f"{text}\n"] + [f" {user}" for user in users])

    def __initialize(self, name: str, days: str, hour: int, minute: int) -> None:
        """
        The core of the Reminder class: This function create a scheduler to
        post self.message and self.card on Discord via a WebRequest.

        Used internally only. Parameters are the same than this class.
        """

        @scheduler.scheduled_job('cron', day_of_week=days, hour=hour, minute=minute, timezone=tz)
        async def job():
            nonlocal self

            channel = self.client.get_channel(CHANNEL_ID)
            async with channel.typing():

                # Append the mentions to the message
                text = self.add_mentions(self.message)

                time.sleep(5)

                # Send through Discord # https://gist.github.com/Vexs/629488c4bb4126ad2a9909309ed6bd71
                message: Message = await channel.send(text, embed=self.card)

                if self.attendance:
                    await message.add_reaction(emoji="\u2705")
                    globals.last_message = message.id

            # Job triggered
            print(f"[!] Job triggered: {datetime.now()} - {name}.")

        # Job registered
        print(f"[+] Job scheduled: {days} @ {hour}h{minute} - {name}.")

    @staticmethod
    def start():
        """Start all schedulers."""
        scheduler.start()
