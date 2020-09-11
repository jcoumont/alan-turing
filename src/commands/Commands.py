
from src import config
from src.web.becode import AttendanceRequest

from typing import Union
from discord import Reaction, User, Member


class Commands:

    def __init__(self) -> None:
        pass

    def initialize(self):

        @config.discord.event
        async def on_ready():
            print(f'[+] Discord.py: {config.discord.user} has connected to Discord!')

        @config.discord.command(name="adduser", pass_context=True)
        async def add_user(context) -> None:
            """User command to activate mentions on appointment reminders."""

            # Retrieve the user
            author = context.message.author.mention

            # Update the database
            config.db.update(author, 'notification', True)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will receive mentions on reminders.")
            await context.send(f"{author} Tu n'as plus besoin de ton cerveau, je te mentionnerai à chaque pointage !")

        @config.discord.command(name="removeuser", pass_context=True)
        async def remove_user(context) -> None:
            """User command to deactivate mentions on appointment reminders."""

            # Retrieve the user
            author = context.message.author.mention

            # Update the database
            config.db.update(author, 'notification', False)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will stop receiving mentions on reminders.")
            await context.send(f"{author} L'oiseau prend son envol ! Je ne te mentionnerai plus les pointages.")

        @config.discord.command(name="addtoken", pass_contexr=True)
        async def add_token(context, token: str) -> None:
            """User command to add its token to the database."""

            # Retrieve the user
            author = context.message.author.mention
            print(author)

            if len(token) > 1:

                # Update the database
                config.db.update(author, 'token', token)

                # Log and send a confirmation to user
                print(f"[!] Token added: {author} added token: {token}")
                await context.send(f"{author}, le token '{token}' a bien été ajouté")

            else:
                await context.send(f"{author}, ton token n'est pas valide.")

        @config.discord.event
        async def on_reaction_add(reaction: Reaction, user: Union[User, Member]):

            if str(reaction.emoji) == "\u2705" \
                    and reaction.message.id == config.last_message \
                    and not user.bot:

                print("[log] User added reaction.")

                # Retrieve the token from the database
                token = config.db.get_token(user.mention)

                if token:
                    token = token[0]

                    # Send an attendance request to Becode
                    if config.last_attendance:

                        attendance = config.last_attendance
                        if AttendanceRequest(attendance[0], attendance[1], token).send():

                            print("[log] Attendance was correctly send.")
                            await user.send(f"{user.mention} J'ai bien pointé pour toi sur Becode !")

                        else:
                            print("[log] Attendance was NOT correctly send.")
                            await user.send(f"{user.mention} OUPS ! Une **erreur** s'est produite... Passe par https://my.becode.org pour pointer.")

        return self

    @staticmethod
    def start() -> None:
        config.discord.run(config.DISCORD_TOKEN)
