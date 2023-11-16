from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from common.enums.status_order import StatusOrder
from models import Courier, Order
from models.courier.repository.courier import courier_repository
from models.order.repository.order import order_repository
from models.order.schemas.order import OrderCreate, OrderINFO, SuccessCreateOrder
from router.deps import PGSession

router = APIRouter()


@router.get('/order/{sid}', response_model=OrderINFO)
async def get_order(session: PGSession, sid: UUID):
    """Get order by sid its status"""
    order = await order_repository.get(session, sid)
    if order:
        return order
    else:
        raise HTTPException(
            status_code=404,
            detail="order not exist",
        )


@router.post('/order/{sid}')
async def compleat_order(session: PGSession, sid: UUID):
    """Compleat order for order_sid"""
    order = await order_repository.get(session, sid)

    if order and order.status != StatusOrder.completed:
        await order_repository.update_order_status(session, sid, with_commit=False)
        await courier_repository.change_order_status(session,
                                                     courier_sid=order.courier_sid,
                                                     with_commit=True)  # remove order for courier
        return 'Success'
    else:
        raise HTTPException(
            status_code=404,
            detail="order completed or not exist",
        )


@router.post('/order', response_model=SuccessCreateOrder)
async def create_order(session: PGSession, order_obj: OrderCreate):
    """Create new order and try to get free courier for it"""
    courier = await session.execute(
        select(Courier).filter(Courier.order_sid.is_(None), Courier.districts.any(order_obj.district))
    )  # getting a courier without an order and with the same district

    courier = courier.scalar()
    if courier:  # if courier exist create order
        new_order = Order(name=order_obj.name,
                          district=order_obj.district,
                          courier_sid=courier.sid)  # create Order object
        order = await order_repository.create(session, new_order, with_commit=True)

        await courier_repository.change_order_status(session=session,
                                                     courier_sid=courier.sid,
                                                     order_sid=order.sid,
                                                     with_commit=True)  # update order data for the courier
        return order
    else:
        raise HTTPException(
            status_code=404,
            detail="courier not found",
        )
