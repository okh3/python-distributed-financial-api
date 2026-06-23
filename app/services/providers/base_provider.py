from abc import ABC, abstractmethod
from models.dto_models import NormalizedFinancialData
from tenacity import retry, stop_after_attempt, wait_exponential

class IProviderStrategy(ABC):
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def execute_with_retry(self) -> NormalizedFinancialData:
        return self.fetch_and_normalize()

    @abstractmethod
    def fetch_and_normalize(self) -> NormalizedFinancialData:
        pass