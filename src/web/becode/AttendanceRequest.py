
import requests
from dataclasses import dataclass
from src.web.becode import TimePeriodsEnum

URL = "https://graph.becode.org/"


@dataclass
class Json:
    """Create and return the JSON structure to post."""

    period: TimePeriodsEnum
    at_home: bool

    def get_json(self):

        return {
            "operationName": "record_attendance_time",
            "variables": {
                "period": self.period.name,
                "atHome": self.at_home
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "553ae433516c13a97e348d4a48dd0114d1949f791ab21d97bed27030a65e85a8"
                }
            }
        }


class AttendanceRequest:

    def __init__(self, period: TimePeriodsEnum, at_home: bool, token: str):

        self.data = Json(period=period, at_home=at_home).get_json()
        self.header = {"Authorization": f"Bearer {token}"}

    def send(self):
        response = requests.post(url=URL, data=self.data, headers=self.header)
        print(response.json())
