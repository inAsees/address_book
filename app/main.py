from fastapi import FastAPI
from app.api.endpoints import addresses
from app.core.config import settings
from app.core.database import engine
from app.models import address
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()

# Create database tables
address.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json"
)

# Include routers
app.include_router(addresses.router, prefix=f"{settings.api_v1_prefix}/addresses", tags=["addresses"])

@app.get("/")
def root():
    return {"message": "Address Book API", "docs": "/docs"}