
from src import Database

from discord.ext.commands import Bot
# from os import environ


class Config:

    def __init__(self):

        # ENV variables
        # self.DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
        # self.DISCORD_CHANNEL_ID = int(environ.get('DISCORD_CHANNEL'))
        # self.WEBHOOK = environ.get('WEBHOOK')
        self.DISCORD_TOKEN = 'NzczMTUxNjE2MTEwODIxNDE2.X6FDjQ.Ogj-Hn3-wA1lSoEtb8bGOmiOXqQ'
        self.DISCORD_CHANNEL_ID = 773154253496909827
        self.WEBHOOK = 'https://discord.com/api/webhooks/773160572308160523/9zmjE75bsOWMGQcKGb2_5P0JBjkuQLfSgrPNx55WxDMkOOAZ_7rhSzTi9qE_b3X-YiK4'

        # Discord client
        self.discord = Bot(command_prefix='!')

        # Database
        self.db = Database()

        # Attendance globals
        self.last_message = None
        self.last_attendance = None  # Attendance (Period, at_home), see >> AttendanceMessage.py


config = Config()
