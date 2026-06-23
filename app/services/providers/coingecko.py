import httpx
from services.providers.base_provider import IProviderStrategy
from models.dto_models import NormalizedFinancialData

class CoinGeckoProvider(IProviderStrategy):
    def __init__(self, coin_id: str):
        self.coin_id = coin_id
        self.url = f"https://api.coingecko.com/api/v3/simple/price?ids={self.coin_id}&vs_currencies=usd"

    def fetch_and_normalize(self) -> NormalizedFinancialData:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(self.url)
            response.raise_for_status()
            data = response.json()
            price = float(data[self.coin_id]["usd"])
            
            return NormalizedFinancialData(
                symbol=self.coin_id.upper(),
                price=price,
                provider="CoinGecko"
            )