from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from tiebreakers import playoffPercentages

# Load env for local dev (in case tiebreakers.py needs it)
load_dotenv()

app = FastAPI(title="Playoff Odds API")

# Validate env vars (for tiebreakers.py)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY env vars")

# Model for calculate-odds
class ScheduleRequest(BaseModel):
    incomplete_games: list[dict]  # e.g., [{"homeTeamId": 1, "awayTeamId": 2, "week": 5, "winner": "home"}]

@app.get("/")
async def root():
    return {"message": "Playoff Odds API is running. Use /update-odds or /calculate-odds."}

@app.post("/update-odds")
async def update_odds():
    """
    Automated trigger: Run sims in tiebreakers.py, which handles all Supabase ops.
    Expects POST body: {} (or any JSON, ignored)
    """
    try:
        results = playoffPercentages({})  # Trigger sims, tiebreakers.py handles Supabase
        return {"status": "success", "message": "Odds updated", "playoff_odds": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-odds")
async def calculate_odds(request: ScheduleRequest):
    """
    User-specific: Run sims with provided schedule and return JSON.
    Expects POST body: {"incomplete_games": [...]}
    """
    try:
        results = playoffPercentages(request.dict())
        return {"playoff_odds": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)