from src import config
from src.web.becode import AttendanceRequest, Locations

import re
from typing import Union
from discord import Reaction, User, Member


class Commands:
    def __init__(self) -> None:
        pass

    def initialize(self):
        @config.discord.event
        async def on_ready():
            print(f"[+] Discord.py: {config.discord.user} has connected to Discord!")

        @config.discord.command(name="adduser", pass_context=True)
        async def add_user(context) -> None:
            """User command to activate mentions on appointment reminders."""

            # Retrieve the user
            mention = context.message.author.mention
            author = self.get_author_id(mention)

            # Update the database
            config.db.update(author, "notification", True)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will receive mentions on reminders.")
            await context.send(
                f"{mention} Tu n'as plus besoin de ton cerveau, je te mentionnerai à chaque pointage !"
            )

        @config.discord.command(name="removeuser", pass_context=True)
        async def remove_user(context) -> None:
            """User command to deactivate mentions on appointment reminders."""

            # Retrieve the user
            mention = context.message.author.mention
            author = self.get_author_id(mention)

            # Update the database
            config.db.update(author, "notification", False)

            # Log and send a confirmation to user
            print(
                f"[!] Mention added: {author} will stop receiving mentions on reminders."
            )
            await context.send(
                f"{mention} L'oiseau prend son envol ! Je ne te mentionnerai plus les pointages."
            )

        @config.discord.command(name="addtoken", pass_contexr=True)
        async def add_token(context, token: str) -> None:
            """User command to add its token to the database."""

            # Retrieve the user
            mention = context.message.author.mention
            author = self.get_author_id(mention)

            if len(token) > 1:

                # Update the database
                config.db.update(author, "token", token)

                # Log and send a confirmation to user
                print(f"[!] Token added: {author} added token: {token}")
                await context.send(f"{mention}, le token '{token}' a bien été ajouté")

            else:
                await context.send(f"{mention}, ton token n'est pas valide.")

        @config.discord.command(name="joke", pass_contexr=True, aliases=["melvin"])
        async def share_joke(context) -> None:
            """User command to share a joke on the channel.
            Joke are as a bot too fun to be private...
            """

            # Retrieve the user
            mention = context.message.author.mention
            author = self.get_author_id(mention)

            # Select a joke from the database
            joke = config.db.get_random_joke()

            if joke:
                # Log and share the joke
                print(f"[!] Joke shared: {author}")
                await context.send(f"{joke}")

        @config.discord.command(name="philo", pass_contexr=True, aliases=["philosophy"])
        async def share_philo(context) -> None:
            """User command to share a joke on the channel.
            Joke are as a bot too fun to be private...
            """

            # Retrieve the user
            mention = context.message.author.mention
            author = self.get_author_id(mention)

            # Select a joke from the database
            philo = config.db.get_random_philo()

            if not philo.empty:
                # Log and share the philo
                print(f"[!] Philo shared: {author}")

                if philo.source == philo.source:  # source known
                    await context.send(
                        f"{philo.quote}\n\n**by** *{philo.author}* in *{philo.source}*"
                    )
                else:  # source unknown
                    await context.send(f"{philo.quote}\n\n**by** *{philo.author}*")

        @config.discord.command(name="python", pass_contexr=True)
        async def share_python(context) -> None:
            """User command to share show python code
            """

            # Retrieve the user
            mention = context.message.author.mention
            author = self.get_author_id(mention)


            await context.send("def hello_world():\n\tprint('Hello World!')")
            
        @config.discord.event
        async def on_reaction_add(reaction: Reaction, user: Union[User, Member]):
            """Event triggered when a user click a reaction to send an attendance to Becode."""

            if reaction.message.id == config.last_message and not user.bot:
                location = None

                # Emoji: House
                if str(reaction.emoji == "\U0001F3E0"):
                    location = Locations.HOME

                # Emoji: City
                elif str(reaction.emoji == "\U0001F307"):
                    location = Locations.BECODE

                if location:
                    print("[!] User added reaction.")

                    # Retrieve the token from the database
                    mention = user.mention
                    author = self.get_author_id(mention)

                    token = config.db.get_token(author)

                    if token:
                        token = token[0]

                        # Send an attendance request to Becode
                        if config.last_attendance:

                            # Init and send the request
                            attendance = config.last_attendance
                            request = AttendanceRequest(attendance[0], location, token)

                            request.start()
                            request.join()

                            if request.get_status():

                                print(
                                    f"[!] Attendance was correctly send for {author}."
                                )
                                await user.send(
                                    f"{mention} J'ai bien pointé pour toi sur Becode !"
                                )

                            else:
                                print(
                                    f"[!] Attendance was NOT correctly send for {author}."
                                )
                                await user.send(
                                    f"{mention} OUPS ! Une **erreur** s'est produite... Passe par https://my.becode.org pour pointer."
                                )

                    else:
                        print(f"[!] Missing token for {author}.")
                        await user.send(
                            f"{mention} OUPS ! Une **erreur** s'est produite: Je n'ai pas trouvé ton token... Tu peux ajouter un token avec la commande **!addtoken**.\nPasse par https://my.becode.org pour le générer"
                        )

        return self

    @staticmethod
    def start() -> None:
        config.discord.run(config.DISCORD_TOKEN)

    @staticmethod
    def get_author_id(mention):
        return re.sub(r"[<>!@]", "", mention)
