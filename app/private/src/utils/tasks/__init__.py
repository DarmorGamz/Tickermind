import asyncio
from datetime import datetime
import os 

async def periodic_task():
    # Pull data here
    data = ...  # Example: fetch data
    asyncio.create_task(add_to_db(data))  # Parallel DB add
    # Log task execution
    os.makedirs('/data', exist_ok=True)  # Create directory if it doesn't exist
    with open('/data/task_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - periodic_task ran\n")

async def add_to_db(data):
    # Add to database here (e.g., using async SQLAlchemy)
    # Log task execution
    os.makedirs('/data', exist_ok=True)  # Create directory if it doesn't exist
    with open('/data/task_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - add_to_db ran\n")