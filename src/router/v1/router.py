from fastapi import APIRouter

from router.v1.courier import courier
from router.v1.order import order

router = APIRouter(prefix="/v1")
router.include_router(courier.router, tags=["курьер"])
router.include_router(order.router, tags=["заказ"])
