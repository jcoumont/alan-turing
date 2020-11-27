
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
        Reminder("Morning meeting", 'mon-fri', 8, 50, True,
                 [MeetMsg("Daily briefing", 10)])
        Reminder("Debrief meeting", 'mon-thu', 16, 40, True,
                 [MeetMsg("Daily debriefing", 10)])

        # Attendances
        Reminder("Pointage 9h - MyBecode", 'mon-fri', 8, 50, True,
                 [AttendanceMsg(Periods.MORNING, Loc.HOME)])
        Reminder("Pointage 12h30 - MyBecode", 'mon-fri', 12, 30, True,
                 [AttendanceMsg(Periods.LUNCH, Loc.HOME)])
        Reminder("Pointage 13h30 - MyBecode", 'mon-fri', 13, 20, True,
                 [AttendanceMsg(Periods.NOON, Loc.HOME)])
        Reminder("Pointage 17h - MyBecode", 'mon-fri', 17, 0,
                 True, [AttendanceMsg(Periods.EVENING, Loc.HOME)])

        # Pauses
        Reminder("Pause 11h - All", 'mon-fri', 11, 0, True, [PauseMsg(15)])
        Reminder("Pause lunch  - All", 'mon-fri', 12, 30, True, [PauseMsg(60)])
        Reminder("Pause 15h - All", 'mon-fri', 15, 0, True, [PauseMsg(15)])

        # Watches
        Reminder("Watch", 'mon-fri', 13, 25, True,
                 [Message("Dans 5 minutes, c'est l'heure du watch! RDV dans le canal `#veilles`")])

        # Réflexions
        # Reminder("Coffee is all you need", 'fri', 8, 46, True,
        #         [Message("sudo get me a coffee")])
        Reminder("Week End", 'fri', 16, 55, True,
                 [Message("Tic... Tac... c'est bientôt le WE! On se revoit lundi. Bisous de loin")])
        Reminder("Play time", 'fri', 15, 50, True,
                 [Message("Dans 5 minutes, c'est l'heure du jeu du vendredi. Rejoingnez-nous pour relâcher la pression de la semaine")])
        # Reminder("Pensée du jour", 'fri', 11, 17, True, [Message("Femme qui met la main à sa conscience ne peut plus dire du mal de sa voisine. | Proverbe.")])
        # Reminder("Citation du jour", 'fri', 13, 39, True, [Message("J'ai le moral à Zorro... C'est comme le moral à zéro mais je suis masqué.")])
        return self

    @staticmethod
    def start():
        Reminder.start()
