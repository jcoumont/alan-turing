from src import config
from src.scheduler.messages import Card, MessageWeight

import time
import random
import operator
from discord import Embed, Message
from pytz import timezone
from typing import NamedTuple, Tuple, List, Union
from src.scheduler.messages import Message
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Initialize apscheduler and setup the timezone.
scheduler = AsyncIOScheduler()
tz = timezone("Europe/Brussels")


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
    Link(message=". Et ", needPoint=False, needUppercase=False),
)


class Reminder:
    def __init__(
        self,
        name: str,
        days: str,
        hour: int,
        minute: int,
        mentions: bool,
        messages: List[Message],
    ):
        """
        Core of this Bot: Create a scheduled element that will send a
        POST request to the Discord webhook.

        :param name: The name of the reminder. For clarity only.
        :param days: Days of the week when this reminder has to trigger.
        :param hour: Hour of the day when this reminder has to trigger.
        :param minute: Minutes of when this reminder has to trigger.
        :param mentions: True if this reminder has to mentions the members.
        :param messages: List of Message object containing the text and
                         card used to generate a Reminder.
        """
        self.mentions = mentions
        self.messages = messages

        self.attendance = self.__retrieve_attendance()
        self.text, self.embed = self.__create_text_embed()

        self.__initialize(name, days, hour, minute)

    def __iter_weight(self):

        for message in self.messages:
            yield message.weight.value, message

    def __create_text_embed(self):

        # Put the messages in a dict with their weight.
        messages = dict(self.__iter_weight())

        # EMBED
        # The embed is taken from the smallest weight message.
        message_embed = None
        card: Union[Card, None] = messages[min(messages)].get_card()

        if card:
            message_embed = card.get_embed()

        # MESSAGE TEXT
        # Sort the messages by higher weight to smaller weight
        sorted_messages = dict(
            sorted(messages.items(), key=operator.itemgetter(0), reverse=True)
        )

        texts = []

        for message in sorted_messages.values():
            texts.append(self.__to_uppercase(message.get_message()))

        message_text = ". ".join(texts) + " !"

        return message_text, message_embed

    def __retrieve_attendance(self):
        """Loop through every message and return the attendance details,
        if they exists."""

        for message in self.messages:
            if message.weight == MessageWeight.ATTENDANCE:

                return message.get_attendance_details()

    @staticmethod
    def get_linker() -> Link:
        """Return a randomly chooser text to link to tenses."""

        return random.choice(linkers)

    @staticmethod
    def __to_uppercase(text: str) -> str:
        """
        Transform the first letter of a given string to uppercase.
        Return the result.
        """

        return "".join([text[0].capitalize(), text[1:]])

    @staticmethod
    def __add_mentions(text: str) -> str:
        """Append the users to mention on a given text."""
        users = config.db.get_users_to_mention()

        # Set users to empty string if the list is empty
        if len(users) == 0:
            users = ""

        # Append the users to mention
        return "".join([f"{text}\n"] + [f" <@{user}>" for user in users])

    def __initialize(self, name: str, days: str, hour: int, minute: int) -> None:
        """
        The core of the Reminder class: This function create a scheduler to
        post self.message and self.card on Discord via a WebRequest.

        Used internally only. Parameters are the same than this class.
        """

        @scheduler.scheduled_job(
            "cron", day_of_week=days, hour=hour, minute=minute, timezone=tz
        )
        async def job():
            nonlocal self

            channel = config.discord.get_channel(config.DISCORD_CHANNEL_ID)

            # Simulate the bot typing during 3 seconds
            async with channel.typing():
                time.sleep(3)

                text = self.text

                # Append the mentions to the message
                if self.mentions:
                    text = self.__add_mentions(text)

                # Send the message and the card through Discord
                # https://gist.github.com/Vexs/629488c4bb4126ad2a9909309ed6bd71
                message: Message = await channel.send(text, embed=self.embed)

                # Add a reaction to the message if the message is
                # attendance related
                if self.attendance:
                    await message.add_reaction(emoji="\U0001F3E0")  # House
                    await message.add_reaction(emoji="\U0001F307")  # City

                    # Save the attendance details
                    config.last_message = message.id
                    config.last_attendance = self.attendance

            # Job triggered
            print(f"[!] Job triggered: {datetime.now()} - {name}.")

        # Job registered
        print(f"[+] Job scheduled: {days} @ {hour}h{minute} - {name}.")

    @staticmethod
    def start():
        """Start all schedulers."""
        scheduler.start()
