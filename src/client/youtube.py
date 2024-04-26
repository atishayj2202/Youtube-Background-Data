import os
from datetime import datetime, timedelta

from googleapiclient.discovery import build

from src.utils.time import parse_time_datetime_to_tz


class YoutubeClient:
    env_var_api_key = "YOUTUBE_API_KEY"
    service_name = "youtube"
    version = "v3"

    def __init__(self):
        self.top = 1
        self.api_key = os.environ[(self.env_var_api_key + str(self.top))]
        self.youtube = build(self.service_name, self.version, developerKey=self.api_key)

    def search_last_hour(self, query: str):
        one_minute_ago = datetime.utcnow() - timedelta(minutes=60)
        request = self.youtube.search().list(
            part="snippet",
            order="date",
            q=query,
            type="video",
            maxResults=20,
            publishedAfter=one_minute_ago.isoformat() + "Z",
        )
        if self.top == 4:
            return [], one_minute_ago
        try:
            response = request.execute()
            response = response.get("items", [])
            self.top = 1
            return response, parse_time_datetime_to_tz(one_minute_ago)
        except:
            self.top += 1
            self.api_key = os.environ[(self.env_var_api_key + str(self.top))]
            self.youtube = build(
                self.service_name, self.version, developerKey=self.api_key
            )
            return self.search_last_hour(query)


if __name__ == "__main__":
    yt = YoutubeClient()
    print(yt.search_last_hour("official"))
