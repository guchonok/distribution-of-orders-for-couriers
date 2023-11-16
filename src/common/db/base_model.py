import uuid

from sqlalchemy import Column, UUID
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    sid = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True, default=lambda: uuid.uuid4().hex,)

    @declared_attr
    def __table__name(self):
        return self.__name__.lower()