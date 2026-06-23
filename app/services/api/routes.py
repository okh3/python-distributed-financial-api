from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from services.redis.tasks import sync_all_financial_data
from services.database.db_context import get_db_session
from services.database.repository import MarketDataRepository
from models.dto_models import MarketDataResponse

router = APIRouter(prefix="/api/v1")

@router.post("/trigger-sync", status_code=status.HTTP_202_ACCEPTED)
def trigger_data_synchronization() -> dict:
    sync_all_financial_data.delay()
    return {"message": "Data sync triggered. Background workers are processing via Redis."}

@router.get("/prices", response_model=List[MarketDataResponse], status_code=status.HTTP_200_OK)
def get_latest_prices(
    limit: int = Query(50, ge=1, le=100, description="Max number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db_session: Session = Depends(get_db_session)
):
    repository = MarketDataRepository(db_session)
    
    records = repository.get_latest_records(limit=limit, offset=offset)
    return records