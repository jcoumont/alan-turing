
from src.reminders import Reminder
from src.reminders.messages import AttendanceMessage, GoogleMeetMessage, PauseMessage
from src.storage import Database
from discord.ext.commands import Bot
from os import environ

DISCORD_TOKEN = environ.get('DISCORD_TOKEN')


class Commands:

    def __init__(self) -> None:
        self.client = Bot(command_prefix='!')
        self.db = Database()

        @self.client.event
        async def on_ready():
            print(f'[+] Discord.py: {self.client.user} has connected to Discord!')

        @self.client.command(name="adduser", pass_context=True)
        async def add_user(context) -> None:
            """User command to activate mentions on appointment reminders."""

            # Retrieve the user
            author = context.message.author.mention

            # Update the database
            self.db.update(author, True)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will receive mentions on reminders.")
            await context.send(f"{author} Tu n'as plus besoin de ton cerveau, je te mentionnerai à chaque pointage !")

        @self.client.command(name="removeuser", pass_context=True)
        async def remove_user(context) -> None:
            """User command to deactivate mentions on appointment reminders."""

            # Retrieve the user
            author = context.message.author.mention

            # Update the database
            self.db.update(author, False)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will stop receiving mentions on reminders.")
            await context.send(f"{author} L'oiseau prend son envol ! Je ne te mentionnerai plus les pointages.")

        self.initialize_reminders()

    def initialize_reminders(self) -> None:

        clt = self.client

        Reminder(clt, "Pointage 9h - Becode", 'mon-sun', 22, 49, True, [AttendanceMessage()])
        Reminder(clt, "Pointage 9h - Becode", 'mon-sun', 22, 50, True, [AttendanceMessage()])
        Reminder(clt, "Pointage 9h - Becode", 'mon-sun', 22, 51, True, [AttendanceMessage()])
        Reminder(clt, "Pointage 9h - Becode", 'mon-sun', 22, 52, True, [AttendanceMessage()])

        # Morning reunions attendances
        Reminder(clt, "Pointage 9h - Becode", 'tue, wed', 8, 50, True, [AttendanceMessage()])
        Reminder(clt, "Pointage 9h - Home", 'mon, thu, fri', 8, 50, True, [GoogleMeetMessage("réunion", 10), AttendanceMessage()])

        # Pauses
        Reminder(clt, "Pause 11h - All", 'mon-fri', 11, 0, False, [PauseMessage(15)])
        Reminder(clt, "Pause 15h - All", 'mon-fri', 15, 0, False, [PauseMessage(15)])

        # Mid-day attendances
        Reminder(clt, "Pointage 12h30 - All", 'mon-fri', 12, 30, True, [AttendanceMessage()])
        Reminder(clt, "Pointage 13h30 - Becode", 'tue, wed', 13, 20, True, [AttendanceMessage()])
        Reminder(clt, "Pointage 13h30 - Home", 'mon, thu, fri', 13, 20, True, [GoogleMeetMessage("veille", 10), AttendanceMessage()])

        # Evening reunions and attendances
        Reminder(clt, "Débriefing 16h45 - Home", 'mon, thu', 16, 35, False, [GoogleMeetMessage("débriefing", 10)])
        Reminder(clt, "Kahoot 16h40 - Home", 'fri', 16, 30, False, [GoogleMeetMessage("kahoot", 10)])
        Reminder(clt, "Pointage 17h00 - All", 'mon-fri', 17, 00, True, [AttendanceMessage()])

    def start(self) -> None:
        Reminder.start()
        self.client.run(DISCORD_TOKEN)
