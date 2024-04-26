import os
from datetime import datetime, timedelta

from googleapiclient.discovery import build

from src.utils.time import (
    get_current_time,
    parse_time_datetime_to_tz,
    parse_time_str_to_tz,
)


class YoutubeClient:
    env_var_api_key = "YOUTUBE_API_KEY"
    service_name = "youtube"
    version = "v3"

    def __init__(self):
        self.api_key = os.environ[self.env_var_api_key]
        self.youtube = build(self.service_name, self.version, developerKey=self.api_key)

    def search_last_hour(self, query: str):
        one_minute_ago = datetime.utcnow() - timedelta(minutes=60)
        request = self.youtube.search().list(
            part="snippet",
            order="date",
            q=query,
            type="video",
            maxResults=50,
            publishedAfter=one_minute_ago.isoformat() + "Z",
        )
        response = request.execute()
        return response, parse_time_datetime_to_tz(one_minute_ago)
