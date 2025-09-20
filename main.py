import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tiebreakers import playoffPercentages, simulate_odds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Playoff Odds API")
logger.info("FastAPI app initialized")

class ScheduleRequest(BaseModel):
    incomplete_games: list[dict]

@app.get("/")
async def root():
    return {"message": "Playoff Odds API is running. Use /update-odds or /calculate-odds."}

@app.post("/update-odds")
async def update_odds():
    try:
        results = playoffPercentages()
        return {"status": "success", "message": "Odds updated", "playoff_odds": results}
    except Exception as e:
        logger.error(f"Error in /update-odds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-odds")
async def calculate_odds(request: ScheduleRequest):
    try:
        results = simulate_odds(request.incomplete_games)
        return {"status": "success", "message": "Odds calculated", "playoff_odds": results}
    except Exception as e:
        logger.error(f"Error in /calculate-odds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
