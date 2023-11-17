import datetime

from sqlalchemy import Column, String, UUID, ForeignKey, ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from common.db.base_model import Base


class Courier(Base):
    __tablename__ = 'couriers'

    name = Column(String, nullable=False)
    districts = Column(ARRAY(String), nullable=False)
    order_sid = Column(UUID(as_uuid=True), ForeignKey('orders.sid'), nullable=True)

    active_order = relationship('Order', foreign_keys=[order_sid], lazy="joined")

    @hybrid_property
    def avg_order_complete_time(self) -> datetime:
        return self._avg_order_complete_time

    @avg_order_complete_time.setter
    def avg_order_complete_time(self, time: datetime):
        self._avg_order_complete_time = time

    @hybrid_property
    def avg_day_orders(self) -> int:
        return self._avg_day_orders

    @avg_day_orders.setter
    def avg_day_orders(self, num_orders: int):
        self._avg_day_orders = num_orders
