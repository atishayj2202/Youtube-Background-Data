from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Record(DBSchemaBase):
    api_call_id: UUID
    title: str
    description: str
    thumbnail_URL: str
    publish_time: datetime

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Record


_Record = Base.from_schema_base(Record, "records")
