from datetime import datetime
from typing import Type

from src.db.base import Base, DBSchemaBase
from src.utils.enums import CallStatus


class ApiCall(DBSchemaBase):
    topic: str
    records: int = 0
    published_after: datetime
    status: CallStatus = CallStatus.SUCCESS

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _ApiCall


_ApiCall = Base.from_schema_base(ApiCall, "api_call")
