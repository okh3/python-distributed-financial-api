# Distributed Financial Aggregator API

A production-ready, asynchronous-task-backed REST API that aggregates real-time market data from multiple third-party financial providers (Stocks, Crypto, Fiat).

This project was built to demonstrate **Enterprise Python Architecture**, emphasizing maintainability, system resilience, and decoupling through SOLID principles.

## 🏗 System Architecture & Design Patterns

Unlike basic CRUD applications, this API separates the fast web server from slow network I/O operations by offloading data ingestion to background workers.

* **Strategy Pattern:** Financial data providers (`AlphaVantage`, `CoinGecko`, `ExchangeRate`) implement a standard `IProviderStrategy` interface. This allows the system to normalize disparate JSON responses into a unified DTO.
* **Factory Pattern:** The `ProviderFactory` dynamically spins up provider classes based on a centralized configuration list, meaning new assets can be tracked without touching core business logic (Open-Closed Principle).
* **Repository Pattern:** Database operations are abstracted into `MarketDataRepository`, decoupling SQL alchemy queries from the FastAPI route controllers.
* **Background Processing:** Heavy network requests are offloaded to **Celery/Redis** workers, ensuring the FastAPI event loop is never blocked by third-party API latency.
* **Resilience:** Network calls utilize the `httpx` library wrapped in `tenacity` decorators to automatically apply exponential backoff and retries for rate-limited or failing external APIs.

## 🛠 Tech Stack

* **Framework:** FastAPI (Python 3)
* **Database:** PostgreSQL & SQLAlchemy (ORM)
* **Task Queue:** Celery & Redis
* **Migrations:** Alembic
* **Validation:** Pydantic
* **Resilience:** HTTPX & Tenacity
* **Logging:** Structlog (JSON-formatted for Datadog/Splunk ingestion)
* **Testing:** Pytest (with `unittest.mock`)
* **Infrastructure:** Docker

## 📂 Project Structure

```text
/python-distributed-financial-api


             
├── docker-compose.yml         # Docker compose
├── requirements.txt           # Required modules
├── /app                       # Core Logic
|   ├── .env                   # Environment variables
│   ├── main.py                # FastAPI application entry point
|   ├── test_api.py            # API Pytest suite
│   ├── /models                # SQLAlchemy Models & Pydantic DTOs
│   ├── /services              # Repositories, Celery Tasks, API Routes
│   ├── /providers             # Provider Strategy & Factory classes
│   ├── /helpers               # Config & Enterprise Structlog setup
|   ├── /alembic               # Database migration scripts
|   ├── alembic.ini            # Migration configuration
```

## 🚀 Quick Start (Docker)

**1. Clone the repository and set up your `.env` file:**
Ensure your `.env` file contains your connection strings:
```ini
DATABASE_URL=postgresql://postgres:mysecretpassword@127.0.0.1:5432/financial_db
REDIS_URL=redis://127.0.0.1:6379/0
ALPHA_VANTAGE_KEY=demo
```

**2. Start the Infrastructure:**
Spin up the PostgreSQL database and Redis broker:
```bash
docker run -d --name fin_data_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=financial_db -p 5432:5432 postgres:15
docker run -d --name fin_data_redis -p 6379:6379 redis:7
```

**3. Run Database Migrations:**
Build the database tables using Alembic:
```bash
python -m alembic upgrade head
```

**4. Start the Application:**
*Start the FastAPI server:*
```bash
uvicorn app.main:app --reload --port 8000
```
*In a separate terminal, start the Celery worker:*
```bash
celery -A app.services.redis.tasks worker --loglevel=info --pool=solo
```

## 🌐 API Endpoints

### `POST /api/v1/trigger-sync`
Triggers an asynchronous background job to fetch the latest market data from all configured providers. 
* **Status:** `202 Accepted`
* **Response:**
```json
{
  "message": "Data sync triggered. Background workers are processing via Redis."
}
```

### `GET /api/v1/prices`
Retrieves normalized market data directly from the PostgreSQL database, ordered by the most recent timestamp.
* **Parameters:** * `limit` (int, default=50): Number of records to return.
  * `offset` (int, default=0): Pagination offset.
* **Status:** `200 OK`
* **Response:**
```json
[
  {
    "id": 1042,
    "symbol": "IBM",
    "price": 145.25,
    "provider": "AlphaVantage",
    "timestamp": "2026-06-23T08:15:30.123456Z"
  },
  {
    "id": 1041,
    "symbol": "BITCOIN",
    "price": 64230.50,
    "provider": "CoinGecko",
    "timestamp": "2026-06-23T08:15:28.987654Z"
  },
  {
    "id": 1040,
    "symbol": "USD/EUR",
    "price": 0.92,
    "provider": "ExchangeRateAPI",
    "timestamp": "2026-06-23T08:15:27.112233Z"
  }
]
```

## 🧪 Testing

The project maintains high test coverage using Pytest. External network calls and Celery task delays are heavily mocked to ensure fast, deterministic testing without relying on live third-party APIs.

Run the test suite from the root directory:
```bash
pytest
```
