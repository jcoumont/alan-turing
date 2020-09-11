
import requests
from src.web.becode import AttendanceJson
from src.web.becode import TimePeriodsEnum

# Debug values:
# import http.client
# URL = "https://postman-echo.com/post"
# http.client.HTTPConnection.debuglevel = 1

URL = "https://graph.becode.org/"


class AttendanceRequest:

    def __init__(self, period: TimePeriodsEnum, at_home: bool, token: str):

        self.data = AttendanceJson(period=period, at_home=at_home).get_json()
        self.header = {"Authorization": f"Bearer {token}"}

    def send(self):
        response = requests.post(url=URL, json=self.data, headers=self.header)
        print("response received")
        return self.return_status(response)

    @staticmethod
    def return_status(response):

        if response.status_code == 200:
            status = response.json()

            if status['data']['recordAttendanceTime']:
                return True

        return False
