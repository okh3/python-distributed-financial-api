from services.redis.celery_app import celery_worker
from services.providers.provider_factory import ProviderFactory
from services.database.db_context import SessionLocal
from services.database.repository import MarketDataRepository
from helpers.logger import get_logger

logger = get_logger(__name__)

@celery_worker.task
def sync_all_financial_data():
    logger.info("Starting background synchronization job...")
    
    providers = ProviderFactory.get_active_providers()

    with SessionLocal() as db_session:
        repository = MarketDataRepository(db_session)
        
        for provider in providers:
            try:
                # We call our new resilient method instead of the raw one
                normalized_data = provider.execute_with_retry() 
                repository.insert_record(normalized_data)
                logger.info(f"Successfully synced {normalized_data.symbol} from {normalized_data.provider}")
                
            except Exception as e:
                # Now it logs the error for this specific coin, but CONTINUES looping 
                # through the rest of the providers instead of killing the whole task!
                logger.error(f"Failed to sync data for provider {provider.__class__.__name__}: {e}")