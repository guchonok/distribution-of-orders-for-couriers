from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models import Order
from models.order.repository.order import order_repository


async def calculate_average_order_metrics(session: AsyncSession, courier_sid: UUID) -> tuple:
    order_list = await order_repository.courier_orders(session, courier_sid)  # list courier`s orders
    avg_day_orders = await get_avg_order_for_day(order_list) if order_list else None  # get avg numbers of order per day

    durations = [(order.completed_at - order.created_at).total_seconds() for order in
                 order_list]  # list avg times durations
    avg_order_complete_time = sum(durations) / len(durations) if order_list else None  # avg time compleat
    return avg_order_complete_time, avg_day_orders


async def get_avg_order_for_day(order_list: List[Order]) -> int:
    order_completed_list = [order.completed_at for order in order_list]
    first_order_date = min(order_completed_list)  # first day, where the order was completed
    last_order_date = max(order_completed_list)  # last day, where the order was completed
    len_order_list = len(order_completed_list)  # number completed courier`s orders

    num_days = (last_order_date - first_order_date).days  # number of days, where the courier carried out the order
    return int(len_order_list / num_days if num_days > 0 else 1)  # if num_days > 0 get 1
