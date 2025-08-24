from datetime import datetime, timedelta
from typing import List
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd


class ApiConnector:
    def __init__(self):
        self.transport = AIOHTTPTransport("https://api.urfonline.com/graphql")
        self.client = Client(transport=self.transport)

    def shows_request(self):
        query = gql("""query ScheduleQuery {
        stream(slug: "urf-online") {
        slate {
            slots {
                show {
                name
                }
            startTime
            endTime
            day
            }
        }
        } 
        }""")
        shows = self.client.execute(query)
        return shows


class Shows:
    def __init__(self):
        shows = ApiConnector().shows_request()
        self.shows = pd.DataFrame(
            [
                {
                    "name": slot["show"]["name"],
                    "start": slot["startTime"],
                    "end": slot["endTime"],
                    "day": slot["day"],
                }
                for slot in shows["stream"]["slate"]["slots"]
            ]
        )

    def __getitem__(self, show_name: str):
        return self.shows[self.shows["name"] == show_name]

    def get_show_times(
        self, show_name: str, start: datetime, end: datetime
    ) -> List[datetime]:
        assert start < end, "Start time must come before end time,"
        show = self[show_name]
        curr = start + timedelta(
            days=(show["day"].item() - start.weekday()) % 7,
            hours=datetime.strptime(show["start"].item(), "%H:%M:%S").hour,
        )

        show_times = []

        while curr < end:
            show_times.append(curr)
            curr += timedelta(days=7)

        return show_times
