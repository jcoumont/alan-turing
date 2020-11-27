import requests
from src.web.becode import AttendanceJson
from src.web.becode import Periods, Locations
from threading import Thread

# Debug values:
# import http.client
# URL = "https://postman-echo.com/post"
# http.client.HTTPConnection.debuglevel = 1

URL = "https://graph.becode.org/"


class AttendanceRequest(Thread):
    def __init__(self, period: Periods, at_home: Locations, token: str):
        Thread.__init__(self)

        self.data = AttendanceJson(period=period, at_home=at_home).get_json()
        self.header = {"Authorization": f"Bearer {token}"}

        self.response = None

    def __send(self):
        self.response = requests.post(url=URL, json=self.data, headers=self.header)

    def run(self):
        self.__send()

    def get_status(self):
        """Return the request status."""

        if self.response.status_code == 200:
            status = self.response.json()

            try:
                if status["data"]["recordAttendanceTime"]:
                    return True

            except KeyError:
                return False

        return False
