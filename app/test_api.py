import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from services.database.db_context import get_db_session
from models.database_models import Base, MarketData
from models.dto_models import NormalizedFinancialData
from services.providers.provider_factory import ProviderFactory


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)

def test_dto_validation_enforces_types():
    data = NormalizedFinancialData(
        symbol="AAPL",
        price=150.50,
        provider="ProviderX"
    )
    assert data.symbol == "AAPL"
    assert type(data.price) is float

@patch('httpx.Client.get')
def test_provider_factory_and_strategy_normalization(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Global Quote": {
            "01. symbol": "IBM",
            "05. price": "145.25"
        }
    }
    mock_response.raise_for_status.return_value = None 
    mock_get.return_value = mock_response
    
    providers = ProviderFactory.get_active_providers() 
    alpha_provider = next(p for p in providers if p.__class__.__name__ == "AlphaVantageProvider")

    result = alpha_provider.fetch_and_normalize()
    assert result.symbol == "IBM"
    assert result.price == 145.25
    assert result.provider == "AlphaVantage"

@patch('services.redis.tasks.sync_all_financial_data.delay')
def test_trigger_sync_endpoint_offloads_to_celery(mock_celery_delay):
    response = client.post("/api/v1/trigger-sync")
    
    assert response.status_code == 202
    assert response.json() == {"message": "Data sync triggered. Background workers are processing via Redis."}

    mock_celery_delay.assert_called_once()

def test_get_prices_endpoint_retrieves_from_database():
    db = TestingSessionLocal()
    test_record = MarketData(symbol="ETH", price=3500.00, provider="CoinGecko")
    db.add(test_record)
    db.commit()
    db.close()
    response = client.get("/api/v1/prices")
    data = response.json()

    assert response.status_code == 200
    assert len(data) >= 1
    assert data[0]["symbol"] == "ETH"
    assert data[0]["price"] == 3500.00
    assert data[0]["provider"] == "CoinGecko"
    assert "timestamp" in data[0]