from src.commands import Commands
from src.scheduler import Scheduler


class Bot:
    def __init__(self):
        self.commands = Commands().initialize()
        self.scheduler = Scheduler().initialize()

    def start(self):
        self.scheduler.start()
        self.commands.start()
