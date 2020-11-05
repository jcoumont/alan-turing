
from src.scheduler import Reminder
from src.scheduler.messages import AttendanceMessage as AttendanceMsg
from src.scheduler.messages import GoogleMeetMessage as MeetMsg
from src.scheduler.messages import PauseMessage as PauseMsg
from src.scheduler.messages import Message
from src.web.becode import Periods
from src.web.becode import Locations as Loc


class Scheduler:

    def __init__(self):
        pass

    def initialize(self):
        # Meetings
        Reminder("Morning meeting", 'mon-fri', 8, 50, True, [MeetMsg("Daily briefing", 10)])
        Reminder("Debrief meeting", 'mon-fri', 16, 50, True, [MeetMsg("Daily debriefing", 10)])

        # Attendances
        Reminder("Pointage 9h - MyBecode", 'mon-fri', 8, 50, True, [AttendanceMsg(Periods.MORNING, Loc.HOME)])
        Reminder("Pointage 12h30 - MyBecode", 'mon-fri', 12, 30, True, [AttendanceMsg(Periods.LUNCH, Loc.HOME)])
        Reminder("Pointage 13h30 - MyBecode", 'mon-fri', 13, 20, True, [AttendanceMsg(Periods.NOON, Loc.HOME)])
        Reminder("Pointage 17h - MyBecode", 'mon-fri', 17, 0, True, [AttendanceMsg(Periods.EVENING, Loc.HOME)])
        
        # Pauses
        Reminder("Pause 11h - All", 'mon-fri', 11, 0, True, [PauseMsg(15)])
        Reminder("Pause lunch  - All", 'mon-fri', 12, 30, True, [PauseMsg(60)])
        Reminder("Pause 15h - All", 'mon-fri', 15, 0, True, [PauseMsg(15)])

        # Watches
        Reminder("Watch", 'mon-fri', 15, 10, True, [Message("Dans 5 minutes, c'est l'heure du watch! RDV dans le canal `#veilles `")])
        
        return self

    @staticmethod
    def start():
        Reminder.start()
