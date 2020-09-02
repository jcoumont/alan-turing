
from threading import Thread
from src.reminders import Reminder
from src.reminders.messages import Message, AttendanceMessage, GoogleMeetMessage, PauseMessage


class Calendar(Thread):

    def __init__(self) -> None:
        """Calendar object: used to initialize the reminders and their content."""
        super().__init__()

    def run(self) -> None:
        self.initialize()

    @staticmethod
    def initialize() -> None:
        """Initialize the reminders and their content."""

        Reminder("Pointage 9h - Becode", 'thu', 0, 20, True, [AttendanceMessage()])
        Reminder("Pointage 9h - Becode", 'thu', 0, 21, True, [AttendanceMessage()])
        Reminder("Pointage 9h - Becode", 'thu', 0, 22, True, [AttendanceMessage()])
        Reminder("Pointage 9h - Becode", 'thu', 0, 23, True, [AttendanceMessage()])

        # Morning reunions attendances
        Reminder("Pointage 9h - Becode", 'tue, wed', 8, 50, True, [AttendanceMessage()])
        Reminder("Pointage 9h - Home", 'mon, thu, fri', 8, 50, True, [GoogleMeetMessage("réunion", 10), AttendanceMessage()])

        # Pauses
        Reminder("Pause 11h - All", 'mon-fri', 11, 0, False, [PauseMessage(15)])
        Reminder("Pause 15h - All", 'mon-fri', 15, 0, False, [PauseMessage(15)])

        # Mid-day attendances
        Reminder("Pointage 12h30 - All", 'mon-fri', 12, 30, True, [AttendanceMessage()])
        Reminder("Pointage 13h30 - Becode", 'tue, wed', 13, 20, True, [AttendanceMessage()])
        Reminder("Pointage 13h30 - Home", 'mon, thu, fri', 13, 20, True, [GoogleMeetMessage("veille", 10), AttendanceMessage()])

        # Evening reunions and attendances
        Reminder("Débriefing 16h45 - Home", 'mon, thu', 16, 35, False, [GoogleMeetMessage("débriefing", 10)])
        Reminder("Kahoot 16h40 - Home", 'fri', 16, 30, False, [GoogleMeetMessage("kahoot", 10)])
        Reminder("Pointage 17h00 - All", 'mon-fri', 17, 00, True, [AttendanceMessage()])

        # ADD MORE REMINDERS HERE
        # -----------------------

        # Basic reminder example:
        # Reminder("A simple reminder", 'mon-fri', 16, 0, False, [Message(("This is reminder with a simple message",))])

        Reminder.start()
