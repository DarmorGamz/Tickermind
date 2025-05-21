from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

# Define a Pydantic model for request/response validation
class MessageResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Hello from the backend!"
            }
        }

# Initialize FastAPI app with custom metadata
app = FastAPI(
    title="Senior Capstone API",
    description="A REST API for the senior capstone project, built with FastAPI.",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",  # ReDoc endpoint (optional alternative UI)
    openapi_url="/openapi.json",  # OpenAPI schema endpoint
)

# Custom Swagger UI parameters
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return app.get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}  # Collapse models by default
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
    # Add custom tags or other schema modifications if needed
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

# Sample endpoint with documentation
@app.get("/", response_model=MessageResponse, summary="Root endpoint", description="Returns a welcome message from the backend.")
async def root():
    return {"message": "Hello from the backend!"}

# Example additional endpoint
@app.get("/health", response_model=MessageResponse, summary="Health check", description="Checks if the API is running.")
async def health():
    return {"message": "API is healthy!"}