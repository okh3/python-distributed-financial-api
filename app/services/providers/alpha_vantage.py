import httpx
from services.providers.base_provider import IProviderStrategy
from models.dto_models import NormalizedFinancialData
from helpers.config import settings

class AlphaVantageProvider(IProviderStrategy):
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.symbol}&apikey={settings.ALPHA_VANTAGE_KEY}"

    def fetch_and_normalize(self) -> NormalizedFinancialData:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(self.url)
            response.raise_for_status()
            data = response.json()
            
            price = float(data["Global Quote"]["05. price"])
            
            return NormalizedFinancialData(
                symbol=self.symbol,
                price=price,
                provider="AlphaVantage"
            )