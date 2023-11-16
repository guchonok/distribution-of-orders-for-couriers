import datetime
from typing import List
from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.enums.status_order import StatusOrder
from common.repository.repository import AbstractRepository
from models.order.order import Order


class OrderRepository(AbstractRepository[Order]):

    async def courier_orders(self, session: AsyncSession, courier_sid: UUID) -> List[Order]:
        orders = await session.execute(
            select(Order).filter(Order.courier_sid == courier_sid, Order.completed_at.is_not(None)))
        return list(orders.scalars().all())

    async def update_order_status(self, session: AsyncSession, order_sid: UUID, with_commit: bool = True) -> None:
        await session.execute(update(Order).where(Order.sid == order_sid).values(status=StatusOrder.completed,
                                                                                 completed_at=datetime.datetime.utcnow()))
        if with_commit:
            await session.commit()
        else:
            await session.flush()


order_repository = OrderRepository(Order)
