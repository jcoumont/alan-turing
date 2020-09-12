
import pickle
import os.path
import pandas as pd
from typing import Any, Union
from dataclasses import dataclass


@dataclass
class Entry:
    """Default database entry, used for new users."""
    user: str
    notification: bool = False
    token: str = None

    def get_list(self):
        return [self.user, self.notification, self.token]


class Database:

    empty = pd.DataFrame(columns=['user', 'notification', 'token'])

    def __init__(self) -> None:
        """Small database used to store if a user want to be notified or not."""

        self.db = self.__initialize_db()

    def __create(self, user: str) -> bool:
        """
        Create a new user to the database.

        :param user: The user to add to the database.
        :return: True if the user was added. False if not.
        """

        if user not in self.db.values:

            self.db.loc[len(self.db)] = Entry(user=user).get_list()
            return True

        return False

    def update(self, user: str, field: str, value: Any) -> None:
        """Update the desired user with the given notification status."""

        # Create the user if it doesn't exists
        if user not in self.db.values:
            status = self.__create(user)

        # Update the desired field
        self.db.loc[self.db['user'] == user, field] = value

        # Save the database to the disk
        self.__save_db()

    def get_users_to_mention(self):
        """Return a list of all user to notify on reminders."""

        notified = self.db[self.db['notification'] == True]
        return notified['user'].values.tolist()

    def get_token(self, user: str) -> Union[str, None]:
        """Return the token of a given user."""

        user_data = self.db[self.db['user'] == user]
        return user_data['token'].values.tolist()

    def __initialize_db(self):
        """Initialize the database once this class is instantiated."""

        # If a database already exists, load it.
        if os.path.isfile('database.p'):
            return self.__load_db()

        # Else, return a new default one.
        else:
            return Database.empty

    def __save_db(self) -> None:
        """Save the database into a "database.p" file."""

        pickle.dump(self.db, open("database.p", "wb"))

    @staticmethod
    def __load_db():
        """Load and return the database from a "database.p" file."""

        return pickle.load(open("database.p", "rb"))
