from typing import TypeVar, Generic, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from interfaces.common.repository.repository import IRepository

T = TypeVar('T')


class AbstractRepository(IRepository, Generic[T]):
    def __init__(self, t_model: type(T)):
        self._t_model = t_model

    async def get(self, session: AsyncSession, sid: UUID) -> T:
        obj = await session.execute(select(self._t_model).filter(self._t_model.sid == sid))
        return obj.scalar()

    async def get_all(self, session: AsyncSession) -> List[T]:
        objs = await session.execute(select(self._t_model))
        return list(objs.scalars().all())

    async def create(self, session: AsyncSession, obj: T, *, with_commit: bool = True) -> T:
        session.add(obj)
        if with_commit:
            await session.commit()
        else:
            await session.flush()
        await session.refresh(obj)
        return obj

    async def update(self, session: AsyncSession, db_obj: T, new_obj: dict) -> T:
        for k in new_obj:
            setattr(db_obj, k, new_obj[k])
        await session.commit()
        return db_obj

    async def delete(self, session: AsyncSession, db_obj: T):
        await session.delete(db_obj)
        await session.commit()
        return

