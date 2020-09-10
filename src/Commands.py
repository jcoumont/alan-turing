
from src import globals
from src.reminders import Reminder
from src.reminders.messages import AttendanceMessage, GoogleMeetMessage, PauseMessage
from src.web.becode import TimePeriodsEnum as Period
from src.web.becode import AttendanceRequest
from src.storage import Database
from typing import Union
from discord.ext.commands import Bot
from discord import Reaction, User, Member
from os import environ

DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
last_message = None


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
            self.db.update(author, 'notification', True)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will receive mentions on reminders.")
            await context.send(f"{author} Tu n'as plus besoin de ton cerveau, je te mentionnerai à chaque pointage !")

        @self.client.command(name="removeuser", pass_context=True)
        async def remove_user(context) -> None:
            """User command to deactivate mentions on appointment reminders."""

            # Retrieve the user
            author = context.message.author.mention

            # Update the database
            self.db.update(author, 'notification', False)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will stop receiving mentions on reminders.")
            await context.send(f"{author} L'oiseau prend son envol ! Je ne te mentionnerai plus les pointages.")

        @self.client.command(name="addtoken", pass_contexr=True)
        async def add_token(context, token: str) -> None:
            """User command to add its token to the database."""

            # Retrieve the user
            author = context.message.author.mention
            print(author)

            if len(token) > 1:

                # Update the database
                self.db.update(author, 'token', token)

                # Log and send a confirmation to user
                print(f"[!] Token added: {author} added token: {token}")
                await context.send(f"{author}, le token '{token}' a bien été ajouté")

            else:
                await context.send(f"{author}, ton token n'est pas valide.")

        @self.client.event
        async def on_reaction_add(reaction: Reaction, user: Union[User, Member]):

            if str(reaction.emoji) == "\u2705" \
                    and reaction.message.id == globals.last_message \
                    and not user.bot:

                # Retrieve the token from the database
                token = self.db.get_token(user.mention)

                if token:
                    token = token[0]

                    # Send an attendance request to Becode
                    if globals.last_attendance:

                        attendance = globals.last_attendance
                        AttendanceRequest(attendance[0], attendance[1], token).send()

        self.initialize_reminders()

    def initialize_reminders(self) -> None:

        clt = self.client

        # Morning reunions and attendances
        Reminder(clt, "Pointage 9h - Becode", 'tue, wed, thu', 8, 50, True, [AttendanceMessage(Period.MORNING, "false")])
        Reminder(clt, "Pointage 9h - Home", 'mon, fri', 8, 50, True, [GoogleMeetMessage("réunion", 10), AttendanceMessage(Period.MORNING, "true")])

        # Pauses
        Reminder(clt, "Pause 11h - All", 'mon-fri', 11, 0, "false", [PauseMessage(15)])
        Reminder(clt, "Pause 15h - All", 'mon-fri', 15, 0, "false", [PauseMessage(15)])

        # Lunch attendances
        Reminder(clt, "Pointage 12h30 - Becode", 'tue, wed, thu', 12, 30, True, [AttendanceMessage(Period.LUNCH, "false")])
        Reminder(clt, "Pointage 12h30 - Home", 'mon, fri', 12, 30, True, [AttendanceMessage(Period.LUNCH, "true")])

        # Noon attendances
        Reminder(clt, "Pointage 13h30 - Becode", 'tue, wed, thu', 13, 29, True, [AttendanceMessage(Period.NOON, "false")])
        Reminder(clt, "Pointage 13h30 - Home", 'mon, fri', 13, 20, True, [GoogleMeetMessage("veille", 10), AttendanceMessage(Period.NOON, "true")])

        # Evening reunions
        Reminder(clt, "Débriefing 16h45 - Home", 'mon, thu', 16, 35, False, [GoogleMeetMessage("débriefing", 10)])
        Reminder(clt, "Kahoot 16h40 - Home", 'fri', 16, 30, False, [GoogleMeetMessage("kahoot", 10)])

        # Evening attendances
        Reminder(clt, "Pointage 17h00 - Becode", 'tue, wed, thu', 17, 00, True, [AttendanceMessage(Period.EVENING, "false")])
        Reminder(clt, "Pointage 17h00 - Home", 'mon, fri', 17, 00, True, [AttendanceMessage(Period.EVENING, "true")])

    def start(self) -> None:
        Reminder.start()
        self.client.run(DISCORD_TOKEN)
