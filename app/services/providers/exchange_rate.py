import httpx
from services.providers.base_provider import IProviderStrategy
from models.dto_models import NormalizedFinancialData

class ExchangeRateProvider(IProviderStrategy):
    def __init__(self, base_currency: str, target_currency: str):
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.url = f"https://open.er-api.com/v6/latest/{self.base_currency}"

    def fetch_and_normalize(self) -> NormalizedFinancialData:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(self.url)
            response.raise_for_status()
            data = response.json()
            
            rate = float(data["rates"][self.target_currency])
            
            return NormalizedFinancialData(
                symbol=f"{self.base_currency}/{self.target_currency}",
                price=rate,
                provider="ExchangeRateAPI"
            )