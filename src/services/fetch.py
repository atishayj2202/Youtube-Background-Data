from uuid import UUID

from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

from src.client.database import DBClient
from src.db.api_call import ApiCall
from src.db.records import Record
from src.utils.time import parse_time_tz_to_str


class FetchService:
    @classmethod
    def fetch_calls(
        cls, db_client: DBClient, templates: Jinja2Templates, request: Request
    ) -> HTMLResponse:
        data = db_client.query(ApiCall.get_all)
        if data is None:
            data = []
        parsed_data = [vars(call) for call in data]
        for i in parsed_data:
            i["created_at"] = parse_time_tz_to_str(i["created_at"])
            i["published_after"] = parse_time_tz_to_str(i["published_after"])
            i["status"] = i["status"].value
        return templates.TemplateResponse(
            "api_call.html", {"data": parsed_data, "request": request}
        )

    @classmethod
    def fetch_call(
        cls,
        db_client: DBClient,
        templates: Jinja2Templates,
        request: Request,
        yt_call_id: UUID,
    ) -> HTMLResponse:
        data = db_client.query(
            Record.get_by_field_multiple,
            field="api_call_id",
            match_value=yt_call_id,
            error_not_exist=False,
        )
        if data is None:
            data = []
        parsed_data = [vars(call) for call in data]
        for i in parsed_data:
            i["publish_time"] = parse_time_tz_to_str(i["publish_time"])
        return templates.TemplateResponse(
            "records.html",
            {"data": parsed_data, "request": request, "id": str(yt_call_id)},
        )
