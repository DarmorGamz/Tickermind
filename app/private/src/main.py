from fastapi import FastAPI
from routers import router as router
from utils.cron import startup, shutdown

app = FastAPI()

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

app.include_router(router.router)