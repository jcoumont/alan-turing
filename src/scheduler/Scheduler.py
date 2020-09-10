
from src.scheduler import Reminder
from src.scheduler.messages import AttendanceMessage, GoogleMeetMessage, PauseMessage
from src.web.becode import TimePeriodsEnum as Period


class Scheduler:

    def __init__(self):
        pass

    def initialize(self):

        # Morning reunions and attendances
        Reminder("Pointage 9h - Becode", 'tue, wed, thu', 8, 50, True, [AttendanceMessage(Period.MORNING, False)])
        Reminder("Pointage 9h - Home", 'mon, fri', 8, 50, True, [GoogleMeetMessage("réunion", 10), AttendanceMessage(Period.MORNING, True)])

        # Pauses
        Reminder("Pause 11h - All", 'mon-fri', 11, 0, False, [PauseMessage(15)])
        Reminder("Pause 15h - All", 'mon-fri', 15, 0, False, [PauseMessage(15)])

        # Lunch attendances
        Reminder("Pointage 12h30 - Becode", 'tue, wed, thu', 12, 30, True, [AttendanceMessage(Period.LUNCH, False)])
        Reminder("Pointage 12h30 - Home", 'mon, fri', 12, 30, True, [AttendanceMessage(Period.LUNCH, True)])

        # Noon attendances
        Reminder("Pointage 13h30 - Becode", 'tue, wed, thu', 13, 20, True, [AttendanceMessage(Period.NOON, False)])
        Reminder("Pointage 13h30 - Home", 'mon, fri', 13, 20, True, [GoogleMeetMessage("veille", 10), AttendanceMessage(Period.NOON, True)])

        # Evening reunions
        Reminder("Débriefing 16h45 - Home", 'mon', 16, 35, False, [GoogleMeetMessage("débriefing", 10)])
        Reminder("Kahoot 16h40 - Home", 'fri', 16, 30, False, [GoogleMeetMessage("kahoot", 10)])

        # Evening attendances
        Reminder("Pointage 17h00 - Becode", 'tue, wed, thu', 17, 00, True, [AttendanceMessage(Period.EVENING, False)])
        Reminder("Pointage 17h00 - Home", 'mon, fri', 17, 00, True, [AttendanceMessage(Period.EVENING, True)])

        return self

    @staticmethod
    def start():
        Reminder.start()
