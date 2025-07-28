from fastapi import FastAPI
from routers import router as router

app = FastAPI()

app.include_router(router.router)