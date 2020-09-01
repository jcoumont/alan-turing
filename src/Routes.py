
from src.reminders import Reminder
from src.reminders.messages import AttendanceMessage, GoogleMeetMessage, PauseMessage


class Routes:

    def __init__(self) -> None:
        """Routes object: used to initialize the reminders and their content."""
        pass

    @staticmethod
    def initialize() -> None:
        """Initialize the reminders and their content."""

        # Morning reunions attendances
        Reminder("Pointage 9h - Becode", 'tue, wed', 8, 50, [AttendanceMessage()])
        Reminder("Pointage 9h - Home", 'mon, thu, fri', 8, 50, [GoogleMeetMessage("réunion", 10), AttendanceMessage()])

        # Pauses
        Reminder("Pause 11h - All", 'mon-fri', 11, 0, [PauseMessage(15)])
        Reminder("Pause 15h - All", 'mon-fri', 15, 0, [PauseMessage(15)])

        # Mid-day attendances
        Reminder("Pointage 12h30 - All", 'mon-fri', 12, 30, [AttendanceMessage()])
        Reminder("Pointage 13h30 - Becode", 'tue, wed', 13, 20, [AttendanceMessage()])
        Reminder("Pointage 13h30 - Home", 'mon, thu, fri', 13, 20, [GoogleMeetMessage("veille", 10), AttendanceMessage()])

        # Evening reunions and attendances
        Reminder("Débriefing 16h45 - Home", 'mon, thu', 16, 35, [GoogleMeetMessage("débriefing", 10)])
        Reminder("Kahoot 16h40 - Home", 'fri', 16, 30, [GoogleMeetMessage("kahoot", 10)])
        Reminder("Pointage 17h00 - All", 'mon-fri', 17, 00, [AttendanceMessage()])

        # ADD MORE REMINDERS HERE
        # -----------------------

        Reminder.start()
