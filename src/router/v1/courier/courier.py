from typing import List
from uuid import UUID

from fastapi import APIRouter

from models import Courier
from models.courier.repository.courier import courier_repository
from models.courier.schemas.courier import CourierCreate, CourierSchema, CourierList

from router.deps import PGSession
from router.v1.courier.ext import calculate_average_order_metrics

router = APIRouter()


@router.get('/courier/{sid}', response_model=CourierSchema)
async def get_courier(session: PGSession, sid: UUID):
    """This endpoint get courier by sid and return full data about him and his orders"""
    courier = await courier_repository.get(session, sid)
    avg_order_complete_time, avg_day_orders = await calculate_average_order_metrics(session,
                                                                                    courier_sid=sid)  # func for get avg compleat order time
    courier.avg_order_complete_time = avg_order_complete_time  # add avg time to hybrid_property model courier
    courier.avg_day_orders = avg_day_orders  # add avg num order per day to hybrid_property model courier
    return courier


@router.get('/couriers', response_model=List[CourierList])
async def get_couriers(session: PGSession):
    """Get all couriers registered in system"""
    couriers = await courier_repository.get_all(session)
    return couriers


@router.post('/courier')
async def create_courier(session: PGSession, courier_obj: CourierCreate):
    """Registration courier in the system and assignment district list to him"""
    new_courier = Courier(name=courier_obj.name, districts=courier_obj.districts)
    courier = await courier_repository.create(session, new_courier, with_commit=True)
    return courier
