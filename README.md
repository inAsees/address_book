# Address Book API

A minimal RESTful API for managing geographic points (addresses) and finding them within a given distance. Built with FastAPI, SQLite, and SQLAlchemy.

## Features

- ✅ Create, read, update, and delete geographic points (latitude/longitude)
- ✅ Input validation for coordinate ranges
- ✅ Find points within a specified distance (km) from given coordinates
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Comprehensive logging (console + optional file)
- ✅ Error handling with appropriate HTTP status codes
- ✅ Auto-generated API documentation (Swagger UI, ReDoc)
- ✅ Docker support for easy deployment
- ✅ Unit tests with pytest

## Technology Stack

- **FastAPI** – Modern web framework
- **SQLAlchemy** – ORM for database operations
- **Pydantic** – Data validation
- **Geopy** – Geodesic distance calculations (Haversine formula)
- **SQLite** – Lightweight database
- **Docker** – Containerization
- **Pytest** – Testing framework

## Project Structure

```text
address-book-api/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── addresses.py  # Route handlers
│   │   └── dependencies.py   # API dependencies (e.g., DB session)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration (pydantic-settings)
│   │   ├── database.py       # Database engine and session
│   │   └── logging_config.py # Logging setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── address.py        # SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── address.py        # Pydantic schemas (request/response)
│   └── services/
│       ├── __init__.py
│       └── address_service.py # Business logic (CRUD, nearby search)
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test fixtures
│   └── test_api/
│       └── test_addresses.py # API endpoint tests
├── .env.example              # Example environment variables
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.12 (for local development)
- Docker (optional, for containerized execution)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/inAsees/address_book
   cd address_book
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv       # On Windows: python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables (optional)**
   Copy `.env.example` to `.env` and adjust settings if needed.
   ```bash
   cp .env.example .env
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
   Interactive documentation: `http://localhost:8000/docs`

---

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t address-book .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 address-book
   ```
   The API will be available at `http://localhost:8000`.

To persist the SQLite database (so data isn't lost when the container stops), mount a local directory:
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app address-book
```
*(Make sure your .env file points to a database path inside /app, e.g., `DATABASE_URL=sqlite:///./address_book.db`.)*

## Environment Variables

The following settings can be configured via environment variables or a `.env` file:

| Variable | Description | Default |
|---|---|---|
| **DATABASE_URL** | SQLite database URL | `sqlite:///./address_book.db` |
| **API_V1_PREFIX** | Prefix for API endpoints | `/api/v1` |
| **PROJECT_NAME** | Project name (used in documentation) | `Address Book API` |
| **LOG_LEVEL** | Logging level (DEBUG, INFO, etc.) | `INFO` |
| **LOG_FORMAT** | Log format (text or json) | `text` |
| **LOG_FILE** | Optional path to a log file | *(none)* |

**Example `.env` file:**
```env
DATABASE_URL=sqlite:///./address_book.db
API_V1_PREFIX=/api/v1
PROJECT_NAME=Address Book API
LOG_LEVEL=INFO
LOG_FORMAT=text
LOG_FILE=app/logs/app.log
```

## API Endpoints

All endpoints are prefixed with `/api/v1/addresses`.

### Create a point
**POST** `/`

Request body (JSON):
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

Response (201 Created):
```json
{
  "id": 1,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "created_at": "2025-03-04T12:00:00",
  "updated_at": null
}
```

### Get a point by ID
**GET** `/{id}`

Response (200 OK):
```json
{
  "id": 1,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "created_at": "2025-03-04T12:00:00",
  "updated_at": null
}
```

### Update a point
**PUT** `/{id}`

Request body (JSON, all fields optional):
```json
{
  "latitude": 40.7580,
  "longitude": -73.9855
}
```
Response (200 OK): updated object.

### Delete a point
**DELETE** `/{id}`

Response: 204 No Content

### Find nearby points
**GET** `/nearby/?latitude={lat}&longitude={lon}&distance_km={km}`

Example:
```http
GET /api/v1/addresses/nearby/?latitude=40.7128&longitude=-74.0060&distance_km=5.0
```

Response (200 OK):
```json
[
  {
    "id": 1,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "created_at": "...",
    "updated_at": null,
    "distance_km": 0.0
  },
  {
    "id": 2,
    "latitude": 40.7580,
    "longitude": -73.9855,
    "created_at": "...",
    "updated_at": null,
    "distance_km": 4.2
  }
]
```

## Testing

Run the test suite with pytest:
```bash
pytest tests/ -v --cov=app
```

For a coverage report in HTML:
```bash
pytest tests/ -v --cov=app --cov-report=html
```

## Design Decisions & Assumptions

- **Minimal data**: Only latitude and longitude are stored – no street/city fields. This keeps the API focused on geographic points.
- **Validation**: Coordinates are validated to be within standard ranges (-90..90, -180..180) using Pydantic.
- **Distance calculation**: Uses `geopy.distance.geodesic`, which implements the accurate Vincenty formula, falling back to the faster but slightly less accurate great‑circle formula if needed. This is more precise than a simple Haversine implementation.
- **Database**: SQLite with SQLAlchemy ORM; coordinates are indexed for performance (implicitly via primary key; no explicit spatial index due to SQLite limitations). For large datasets, consider a spatial database like PostGIS.
- **Logging**: Configured to log to console and optionally to a rotating file. Log levels can be adjusted via environment variables.
- **Error handling**: Returns appropriate HTTP status codes (400, 404, 422, 500) with descriptive messages.
- **Docker**: The Dockerfile uses a slim Python image and installs only production dependencies; the app runs with Uvicorn.

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'sqlalchemy'**
Ensure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

**Database file not writable**
When using Docker with a mounted volume, ensure the directory exists and has write permissions. The app will create the `.db` file if needed.

**Port already in use**
Change the port mapping: `docker run -p 8080:8000 ...` and access at `http://localhost:8080`.

**Geodesic distance errors**
If you remove `geopy` from requirements, replace the distance calculation with a manual Haversine formula. The current implementation expects geopy to be installed.

