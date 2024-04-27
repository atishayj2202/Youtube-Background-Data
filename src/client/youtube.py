import os
from datetime import datetime, timedelta

from googleapiclient.discovery import build

from src.utils.time import parse_time_datetime_to_tz


class YoutubeClient:
    env_var_api_key = "YOUTUBE_API_KEY"
    service_name = "youtube"
    version = "v3"

    def __init__(self):
        self.top = 0
        self.youtube = []
        for i in range(1, 4):
            self.api_key = os.environ[(self.env_var_api_key + str(i))]
            self.youtube.append(
                build(self.service_name, self.version, developerKey=self.api_key)
            )

    def search_last_hour(self, query: str):
        one_minute_ago = datetime.utcnow() - timedelta(minutes=60)
        request = (
            self.youtube[self.top]
            .search()
            .list(
                part="snippet",
                order="date",
                q=query,
                type="video",
                maxResults=20,
                publishedAfter=one_minute_ago.isoformat() + "Z",
            )
        )
        if self.top == 3:
            return [], one_minute_ago
        try:
            response = request.execute()
            response = response.get("items", [])
            self.top = 0
            return response, parse_time_datetime_to_tz(one_minute_ago)
        except:
            self.top += 1
            return self.search_last_hour(query)


if __name__ == "__main__":
    yt = YoutubeClient()
    print(yt.search_last_hour("official"))
