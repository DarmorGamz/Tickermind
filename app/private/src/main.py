from fastapi import FastAPI
from routers import router as router
from utils.cron import startup, shutdown

# Create API
app = FastAPI()

# Add Crons & Tasks
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

# Define routers
app.include_router(router.router)