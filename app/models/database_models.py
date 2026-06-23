from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Index
from datetime import datetime, timezone

Base = declarative_base()

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    price = Column(Numeric(18, 4), nullable=False)
    provider = Column(String(50), nullable=False)
    
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


    __table_args__ = (
        Index("ix_market_data_symbol_time", "symbol", "timestamp"),
    )