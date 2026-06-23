from services.providers.alpha_vantage import AlphaVantageProvider
from services.providers.coingecko import CoinGeckoProvider
from services.providers.exchange_rate import ExchangeRateProvider
from helpers.config import settings

class ProviderFactory:
    @staticmethod
    def get_active_providers() -> list:
        providers = []
        for asset in settings.TRACKED_ASSETS:
            if asset["type"] == "stock":
                providers.append(AlphaVantageProvider(symbol=asset["symbol"]))
            elif asset["type"] == "crypto":
                providers.append(CoinGeckoProvider(coin_id=asset["id"]))
            elif asset["type"] == "fiat":
                providers.append(ExchangeRateProvider(base_currency=asset["base"], target_currency=asset["target"]))
        
        return providers