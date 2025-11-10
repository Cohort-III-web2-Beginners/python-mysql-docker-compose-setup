from fastapi import FastAPI, status, HTTPException
from datetime import datetime
from typing import List, Optional, Dict
from .database import db
from . import queries
from .controller import home
import logging
import time

logger = logging.getLogger(__name__)

app = FastAPI(
    title = "Todo App",
    version = "0.0.1",
    description = "Our Integrated docker fastApi + mySQL"
    )

database_ready = False

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    global database_ready
    
    logger.info("Starting application...")
    
    # Wait for database with retry logic
    max_retries = 30
    for attempt in range(max_retries):
        try:
            logger.info(f"Database connection attempt {attempt + 1}/{max_retries}")
            
            # Test if database is ready first
            if db.wait_for_db(max_retries=1, retry_interval=2):
                # Then create tables
                with db.get_cursor() as cursor:
                    cursor.execute(queries.CREATE_USERS_TABLE)
                    logger.info("users table initialized successfully")
                
                database_ready = True
                logger.info("🎉 Application started successfully!")
                break
            else:
                raise Exception("Database not ready")
            
        except Exception as e:
            logger.warning(f"⚠️ Startup attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = 5
                logger.info(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
    else:
        logger.error("Failed to connect to database after all retries")
        database_ready = False
        # Don't raise exception - let the app start and retry on first request




# @app.get("/")(home)