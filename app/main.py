from fastapi import FastAPI
from helpers.logger import get_logger
from services.api.routes import router
from services.database.db_context import engine
from models.database_models import Base

logger = get_logger(__name__)

app = FastAPI(title="Distributed Financial Aggregator (SOLID Architecture)")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)