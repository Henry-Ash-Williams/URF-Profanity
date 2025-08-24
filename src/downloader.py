from datetime import datetime
from os import PathLike
import requests


class ShowDownloader:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @staticmethod
    def generate_url(time: datetime):
        return f"https://archive.urfonline.com/{time.year}/{time.month:02}/{time.day:02}/{time.hour:02}.mp3"

    def download(self, time: datetime, output: PathLike):
        url = self.generate_url(time)
        res = requests.get(url, auth=(self.username, self.password))

        if not res.ok:
            raise FileNotFoundError("Could not find a show at this time")

        with open(output, "wb") as f:
            f.write(res.content)
