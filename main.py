import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from tiebreakers import playoffPercentages, simulate_odds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load env for local dev
load_dotenv()
logger.info("Loaded environment variables from .env file")

# Initialize FastAPI
app = FastAPI(title="Playoff Odds API")
logger.info("FastAPI app initialized")

# Validate env vars
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
PORT = os.getenv("PORT", "10000")
logger.info(f"SUPABASE_URL: {SUPABASE_URL}")
logger.info(f"SUPABASE_SERVICE_ROLE_KEY: {'[REDACTED]' if SUPABASE_SERVICE_ROLE_KEY else None}")
logger.info(f"PORT: {PORT}")
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    logger.error("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY env vars")
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY env vars")

# Model for calculate-odds
class ScheduleRequest(BaseModel):
    incomplete_games: list[dict]  # e.g., [{"homeTeamId": 1, "awayTeamId": 2, "week": 5, "winner": "home"}]

@app.get("/")
async def root():
    logger.info("Received GET request to /")
    return {"message": "Playoff Odds API is running. Use /update-odds or /calculate-odds."}

@app.post("/update-odds")
async def update_odds():
    """
    Automated trigger: Run sims in tiebreakers.py, which handles all Supabase ops.
    Expects POST body: {} (or any JSON, ignored)
    """
    logger.info("Received POST request to /update-odds")
    try:
        results = playoffPercentages()
        logger.info("Successfully ran playoffPercentages")
        return {"status": "success", "message": "Odds updated", "playoff_odds": results}
    except Exception as e:
        logger.error(f"Error in /update-odds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-odds")
async def calculate_odds(request: ScheduleRequest):
    """
    User-specific: Run sims with provided schedule and return JSON.
    Expects POST body: {"incomplete_games": [...]}
    """
    logger.info(f"Received POST request to /calculate-odds with body: {request.dict()}")
    try:
        results = simulate_odds()
        logger.info("Successfully ran simulate_odds")
        return {"status": "success", "message": "Odds updated", "playoff_odds": results}
    except Exception as e:
        logger.error(f"Error in /calculate-odds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

#if __name__ == "__main__":
#    import uvicorn
#    port = int(PORT)
#    logger.info(f"Starting Uvicorn on 0.0.0.0:{port}")
#    try:
#        uvicorn.run(app, host="0.0.0.0", port=port)
#    except Exception as e:
#        logger.error(f"Failed to start Uvicorn: {str(e)}")
#        raise