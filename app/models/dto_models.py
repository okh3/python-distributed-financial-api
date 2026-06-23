from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class NormalizedFinancialData(BaseModel):
    symbol: str
    price: float
    provider: str
    timestamp: Optional[datetime] = None


class MarketDataResponse(BaseModel):
    id: int
    symbol: str
    price: float
    provider: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)