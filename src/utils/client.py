from src.client.cockroach import CockroachDBClient

cockroachClient = None


def getCockroachClient() -> CockroachDBClient:
    global cockroachClient
    if cockroachClient is None:
        cockroachClient = CockroachDBClient()
    return cockroachClient
