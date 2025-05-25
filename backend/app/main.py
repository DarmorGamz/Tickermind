from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List
import random

# Define Pydantic models for stocks and columns
class Stock(BaseModel):
    symbol: str
    name: str
    price: float
    changePercent: float
    volume: int
    marketCap: int
    peRatio: float

    class Config:
        schema_extra = {
            "example": {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "price": 145.30,
                "changePercent": 2.15,
                "volume": 12500000,
                "marketCap": 2400000000000,
                "peRatio": 28.4
            }
        }

class ColumnConfig(BaseModel):
    id: str
    label: str
    optional: bool

    class Config:
        schema_extra = {
            "example": {
                "id": "symbol",
                "label": "Symbol",
                "optional": False
            }
        }

class MessageResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Hello from the backend!"
            }
        }

# Initialize FastAPI app
app = FastAPI(
    title="Senior Capstone API",
    description="A REST API for the senior capstone project, built with FastAPI.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allowed methods
    allow_headers=["Content-Type", "Authorization"],  # Allowed headers
)

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return app.get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}
    )

# Customize OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["info"]["contact"] = {
        "name": "Capstone Team",
        "email": "team@example.com",
    }
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Sample stock data (replace with database or external API in production)
stock_data = [
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 145.30,
        "changePercent": 2.15,
        "volume": 12500000,
        "marketCap": 2400000000000,
        "peRatio": 28.4
    },
    {
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "price": 2750.10,
        "changePercent": -1.25,
        "volume": 8700000,
        "marketCap": 1800000000000,
        "peRatio": 32.1
    },
    {
        "symbol": "MSFT",
        "name": "Microsoft Corp.",
        "price": 305.45,
        "changePercent": 0.95,
        "volume": 10200000,
        "marketCap": 2300000000000,
        "peRatio": 35.7
    },
    {
        "symbol": "AMZN",
        "name": "Amazon.com Inc.",
        "price": 3122.90,
        "changePercent": -0.78,
        "volume": 9500000,
        "marketCap": 1600000000000,
        "peRatio": 41.2
    },
    {
        "symbol": "META",
        "name": "Meta Platforms Inc.",
        "price": 321.65,
        "changePercent": 1.42,
        "volume": 7800000,
        "marketCap": 850000000000,
        "peRatio": 25.8
    },
    {
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "price": 734.20,
        "changePercent": 3.28,
        "volume": 15600000,
        "marketCap": 780000000000,
        "peRatio": 58.3
    },
    {
        "symbol": "NFLX",
        "name": "Netflix Inc.",
        "price": 625.80,
        "changePercent": -2.10,
        "volume": 5400000,
        "marketCap": 275000000000,
        "peRatio": 43.5
    },
    {
        "symbol": "NVDA",
        "name": "NVIDIA Corp.",
        "price": 215.75,
        "changePercent": 4.32,
        "volume": 18900000,
        "marketCap": 540000000000,
        "peRatio": 63.8
    }
]

columns = [
    {"id": "symbol", "label": "Symbol", "optional": False},
    {"id": "price", "label": "Price", "optional": False},
    {"id": "changePercent", "label": "Change %", "optional": False},
    {"id": "volume", "label": "Volume", "optional": True},
    {"id": "marketCap", "label": "Market Cap", "optional": True},
    {"id": "peRatio", "label": "P/E Ratio", "optional": True}
]

# Endpoints
@app.get("/", response_model=MessageResponse, summary="Root endpoint", description="Returns a welcome message from the backend.")
async def root():
    return {"message": "Hello from the backend!"}

@app.get("/health", response_model=MessageResponse, summary="Health check", description="Checks if the API is running.")
async def health():
    return {"message": "API is healthy!"}

@app.get("/api/stocks", response_model=List[Stock], summary="Get stock data", description="Returns a list of stock data.")
async def get_stocks():
    # Simulate price updates for polling
    updated_stocks = [
        {**stock, "price": stock["price"] * (1 + (random.random() - 0.5) * 0.01)}
        for stock in stock_data
    ]
    return updated_stocks

@app.get("/api/columns", response_model=List[ColumnConfig], summary="Get column configuration", description="Returns the column configuration for the stock table.")
async def get_columns():
    return columns