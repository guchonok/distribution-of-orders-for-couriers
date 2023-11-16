from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from common.repository.repository import AbstractRepository
from models.courier.courier import Courier


class CourierRepository(AbstractRepository[Courier]):

    async def change_order_status(self, session: AsyncSession,
                            courier_sid: UUID,
                            order_sid: UUID | None = None,
                            with_commit: bool = True) -> None:
        if order_sid:
            await session.execute(update(Courier).where(Courier.sid == courier_sid).values(order_sid=order_sid))
        else:
            await session.execute(update(Courier).where(Courier.sid == courier_sid).values(order_sid=None))

        if with_commit:
            await session.commit()
        else:
            await session.flush()


courier_repository = CourierRepository(Courier)
