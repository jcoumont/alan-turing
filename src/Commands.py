
from src.storage import Database
from discord.ext.commands import Bot
from os import environ


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

    def start(self) -> None:
        self.client.run(environ.get('DISCORD'))
