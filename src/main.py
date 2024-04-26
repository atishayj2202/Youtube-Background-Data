import os
import threading
import time
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from src.client.database import DBClient
from src.services.fetch import FetchService
from src.services.youtube import YoutubeService
from src.utils.client import getDBClient, getYoutubeClient

app = FastAPI(title="Air It Backend", version="0.1.0")

origins = os.environ["CORS_ORIGINS"].split(",")


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()

        try:
            response = await call_next(request)
        except HTTPException as exc:
            response = exc

        end_time = time.time()
        process_time = end_time - start_time
        print(
            f"Request {request.method} {request.url} processed in {process_time:.5f} seconds"
        )

        return response


app.add_middleware(TimingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    getDBClient()

    def backgorund_yt_update():
        while True:
            temp_db_client = DBClient()
            try:
                YoutubeService.update_records(
                    db_client=temp_db_client, youtube_client=getYoutubeClient()
                )
            except:
                pass
            temp_db_client.dispose()
            del temp_db_client
            time.sleep(60)

    thread = threading.Thread(target=backgorund_yt_update)
    thread.daemon = True
    thread.start()


templates = Jinja2Templates(directory="templates")


@app.get("/calls", response_class=HTMLResponse)
async def get_calls(request: Request, db_client: DBClient = Depends(getDBClient)):
    return FetchService.fetch_calls(
        db_client=db_client, templates=templates, request=request
    )


@app.get("/call/{yt_call_id}", response_class=HTMLResponse)
async def get_calls(
    request: Request, yt_call_id: UUID, db_client: DBClient = Depends(getDBClient)
):
    return FetchService.fetch_call(
        db_client=db_client, templates=templates, request=request, yt_call_id=yt_call_id
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=80, reload=True)
