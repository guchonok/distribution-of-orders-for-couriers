from uuid import UUID

from pydantic import BaseModel

from common.enums.status_order import StatusOrder


class OrderBase(BaseModel):
    name: str
    district: str


class OrderInfoCourier(BaseModel):  # schema for courier order info
    sid: UUID
    name: str


class OrderCreate(OrderBase):
    ...


class OrderINFO(BaseModel):
    courier_sid: UUID
    status: StatusOrder


class SuccessCreateOrder(BaseModel):
    sid: UUID
    courier_sid: UUID


class CourierSchema(OrderBase):
    courier_sid: UUID
