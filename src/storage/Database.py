
import pickle
import os.path
import pandas as pd


class Database:

    default = pd.DataFrame(columns=['user', 'notification'])

    def __init__(self) -> None:
        """Small database used to store if a user want to be notified or not."""

        self.db = self.__initialize_db()
        print(self.db)

    def update(self, user: str, notification: bool) -> None:
        """Update the desired user with the given notification status."""

        # If the user is already in db, update is
        if user in self.db.values:
            self.db.loc[self.db['user'] == user, 'notification'] = notification

        # If not, create it
        else:
            self.db.loc[len(self.db)] = [user, notification]

        self.__save_db()

    def get_users_to_mention(self):
        """Return a list of all user to notify on reminders."""

        notified = self.db[self.db['notification'] == True]
        return notified['user'].values.tolist()

    def __initialize_db(self):
        """Load the database when this class in instantiated."""

        # If a database already exists, load it.
        if os.path.isfile('database.p'):
            return self.__load_db()

        # Else, return a new default one.
        else:
            return Database.default

    def __save_db(self) -> None:
        """Save the database into a "database.p" file."""

        pickle.dump(self.db, open("database.p", "wb"))

    @staticmethod
    def __load_db():
        """Load and return the database from a "database.p" file."""

        return pickle.load(open("database.p", "rb"))
