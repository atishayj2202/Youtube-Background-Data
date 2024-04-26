from src.client.database import DBClient
from src.client.youtube import YoutubeClient
from src.db.api_call import ApiCall
from src.db.records import Record
from src.utils.enums import CallStatus
from src.utils.time import get_current_time, parse_time_str_to_tz


class YoutubeService:
    @classmethod
    def update_records(cls, db_client: DBClient, youtube_client: YoutubeClient):
        query = "official"
        try:
            youtube_videos, after_publish_time = youtube_client.search_last_hour(query)
            call_record: ApiCall = ApiCall(
                topic=query,
                records=len(youtube_videos),
                published_after=after_publish_time,
                status=CallStatus.SUCCESS if youtube_videos else CallStatus.NOT_FOUND,
            )
            parsed_videos = [
                Record(
                    api_call_id=call_record.id,
                    title=video["snippet"]["title"],
                    description=video["snippet"]["description"],
                    thumbnail_url=video["snippet"]["thumbnails"]["default"]["url"],
                    channel_id=video["snippet"]["channelId"],
                    channel_name=video["snippet"]["channelTitle"],
                    video_id=video["id"]["videoId"],
                    publish_time=parse_time_str_to_tz(video["snippet"]["publishedAt"]),
                )
                for video in youtube_videos
            ]
            db_client.queries(
                fn=[ApiCall.add, Record.add],
                kwargs=[{"items": [call_record]}, {"items": parsed_videos}],
            )
        except:
            call_record: ApiCall = ApiCall(
                topic=query,
                published_after=get_current_time(),
                status=CallStatus.FAILED,
            )
            print("Failed to update Youtube records")
            db_client.query(
                ApiCall.add,
                items=[call_record],
            )
