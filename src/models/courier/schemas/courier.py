import datetime
from uuid import UUID

from pydantic import BaseModel

from models.order.schemas.order import OrderInfoCourier


class CourierBase(BaseModel):
    name: str


class CourierList(CourierBase):
    sid: UUID


class CourierCreate(CourierBase):
    districts: list[str]


class CourierSchema(CourierBase):
    sid: UUID
    active_order: OrderInfoCourier | None
    avg_order_complete_time: datetime.time | None
    avg_day_orders: int | None


class CourierUpdate(BaseModel):
    order_sid: UUID
