from src.client.database import DBClient
from src.client.youtube import YoutubeClient

db_client = None
yt_client = None


def getDBClient() -> DBClient:
    global db_client
    if db_client is None:
        db_client = DBClient()
    return db_client


def getYoutubeClient() -> YoutubeClient:
    global yt_client
    if yt_client is None:
        yt_client = YoutubeClient()
    return yt_client
