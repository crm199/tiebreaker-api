import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from tiebreakers import playoffPercentages, simulate_odds

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load env vars
load_dotenv()
logger.info("Loaded environment variables")

# Validate env vars
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
logger.info(f"SUPABASE_URL: {SUPABASE_URL}")
logger.info(f"SUPABASE_KEY: {'[REDACTED]' if SUPABASE_KEY else None}")
if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Missing SUPABASE_URL or SUPABASE_KEY")
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY")

# FastAPI app
app = FastAPI()
logger.info("FastAPI app initialized")

# Request model
class ScheduleRequest(BaseModel):
    incomplete_games: list[dict]

# Routes
@app.get("/")
async def root():
    logger.info("GET / called")
    return {"message": "Server is running. Use /update-odds or /calculate-odds."}

@app.post("/update-odds")
async def update_odds():
    logger.info("POST /update-odds called")
    try:
        results = playoffPercentages()
        logger.info("playoffPercentages ran successfully")
        return {"status": "success", "playoff_odds": results}
    except Exception as e:
        logger.error(f"Error in /update-odds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-odds")
async def calculate_odds(request: ScheduleRequest):
    logger.info(f"POST /calculate-odds called with body: {request.dict()}")
    try:
        results = simulate_odds(request.incomplete_games)
        logger.info("simulate_odds ran successfully")
        return {"status": "success", "playoff_odds": results}
    except Exception as e:
        logger.error(f"Error in /calculate-odds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))