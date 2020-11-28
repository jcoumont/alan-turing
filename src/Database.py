import pickle
import random
import os.path
import pandas as pd
from typing import Any, Union
from dataclasses import dataclass


DB_PATH = "./db/database.p"
DB_PHILO_PATH = "./db/philosophy_quotes.csv"
DB_JOKES_PATH = "./db/bad_jokes.csv"


@dataclass
class Entry:
    """Default database entry, used for new users."""

    user: str
    notification: bool = False
    token: str = None

    def get_list(self):
        return [self.user, self.notification, self.token]


class Database:

    empty = pd.DataFrame(columns=["user", "notification", "token"])
    empty_philo = pd.DataFrame(columns=["quote", "author", "source"])
    empty_jokes = pd.DataFrame(columns=["joke", "category"])

    def __init__(self) -> None:
        """Small database used to store :
        - if a user want to be notified or not.
        - the philosophy quotes
        - the 'jokes à papa'/bad jokes
        """

        self.db = self.__initialize_db()
        self.db_philo = self.__initialize_db_philo()
        self.db_jokes = self.__initialize_db_jokes()

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
        self.db.loc[self.db["user"] == user, field] = value

        # Save the database to the disk
        self.__save_db()

    def get_users_to_mention(self):
        """Return a list of all user to notify on reminders."""

        notified = self.db[self.db["notification"] == True]
        return notified["user"].values.tolist()

    def get_token(self, user: str) -> Union[str, None]:
        """Return the token of a given user."""

        user_data = self.db[self.db["user"] == user]
        return user_data["token"].values.tolist()

    def __initialize_db(self):
        """Initialize the database once this class is instantiated."""

        # If a database already exists, load it.
        if os.path.isfile(DB_PATH):
            return self.__load_db()

        # Else, return a new default one.
        else:
            return Database.empty

    def __save_db(self) -> None:
        """Save the database into a "database.p" file."""

        pickle.dump(self.db, open(DB_PATH, "wb"))

    @staticmethod
    def __load_db():
        """Load and return the database from a "database.p" file."""

        return pickle.load(open(DB_PATH, "rb"))

    def __initialize_db_philo(self):
        """Initialize the database philo once this class is instantiated."""

        # If a database already exists, load it.
        if os.path.isfile(DB_PHILO_PATH):
            return self.__load_db_philo()

        # Else, return a new default one.
        else:
            return Database.empty_philo

    def __save_db_philo(self) -> None:
        """Save the database philo into a "philosophy_quotes.csv" file."""
        pd.to_csv(DB_PHILO_PATH)

    @staticmethod
    def __load_db_philo():
        """Load and return the database from a "philosophy_qutes.csv" file."""
        return pd.read_csv(DB_PHILO_PATH)

    def __initialize_db_jokes(self):
        """Initialize the database jokes once this class is instantiated."""

        # If a database already exists, load it.
        if os.path.isfile(DB_JOKES_PATH):
            return self.__load_db_jokes()

        # Else, return a new default one.
        else:
            return Database.empty_jokes

    def __save_db_jokes(self) -> None:
        """Save the database jokes into a "bad_jokes.csv" file."""
        pd.to_csv(DB_JOKES_PATH)

    @staticmethod
    def __load_db_jokes():
        """Load and return the database from a "bad_jokes.csv" file."""
        return pd.read_csv(DB_JOKES_PATH)

    def get_random_joke(self, category: str = None):
        if self.db_jokes is None or len(self.db_jokes.index) == 0:
            return None
        else:
            if category:
                jokes = self.db_jokes[self.db_jokes.category == category]
            else:
                jokes = self.db_jokes
            r_int = random.randint(0, len(jokes.index))
            idx = jokes.index[r_int]
            return jokes.loc[idx, "joke"]

    def get_random_philo(self):
        if self.db_philo is None or len(self.db_philo.index) == 0:
            return None
        else:
            r_int = random.randint(0, len(self.db_philo.index))
            idx = self.db_philo.index[r_int]
            return self.db_philo.loc[idx, :]
