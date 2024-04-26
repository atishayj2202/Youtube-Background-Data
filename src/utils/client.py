from src.client.database import DBClient

db_client = None


def getCockroachClient() -> DBClient:
    global db_client
    if db_client is None:
        db_client = DBClient()
    return db_client
