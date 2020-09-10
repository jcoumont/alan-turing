
from src import Database

from discord.ext.commands import Bot
from os import environ


class Config:

    def __init__(self):

        # ENV variables
        self.DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
        self.DISCORD_CHANNEL_ID = int(environ.get('DISCORD_CHANNEL'))
        self.WEBHOOK = environ.get('WEBHOOK')

        # Discord client
        self.discord = Bot(command_prefix='!')

        # Database
        self.db = Database()

        # Attendance globals
        self.last_message = None
        self.last_attendance = None  # Attendance (Period, at_home), see >> AttendanceMessage.py


config = Config()
