from sqlalchemy.orm import Session
from models.database_models import MarketData
from models.dto_models import NormalizedFinancialData

class MarketDataRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def insert_record(self, data: NormalizedFinancialData) -> MarketData:
        new_record = MarketData(
            symbol=data.symbol,
            price=data.price,
            provider=data.provider
        )
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        return new_record

    def get_latest_records(self, limit: int = 50, offset: int = 0) -> list[MarketData]:
        return self.db.query(MarketData)\
                      .order_by(MarketData.timestamp.desc())\
                      .offset(offset)\
                      .limit(limit)\
                      .all()