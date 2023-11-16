from common.db.base_model import Base

# include models here

from models.courier.courier import Courier  # noqa
from models.order.order import Order  # noqa


metadata = Base.metadata