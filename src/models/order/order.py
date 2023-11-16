import datetime

from sqlalchemy import Column, String, ForeignKey, UUID, Integer, DateTime, Enum

from common.db.base_model import Base
from common.enums.status_order import StatusOrder


class Order(Base):
    __tablename__ = 'orders'

    name = Column(String, nullable=False)
    status = Column(Enum(StatusOrder, name='order_status_enum', create_type=False),
                    nullable=False, default=StatusOrder.in_progress)
    district = Column(String, nullable=False)
    courier_sid = Column(UUID(as_uuid=True), ForeignKey('couriers.sid'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
