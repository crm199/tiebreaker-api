from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from tiebreakers import simulate_odds  # Match deployed import

# Load env for local dev
load_dotenv()

app = FastAPI(title="Playoff Odds API")

# Supabase config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY env vars")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Model for calculate-odds
class ScheduleRequest(BaseModel):
    incomplete_games: list[dict]  # e.g., [{"homeTeamId": 1, "awayTeamId": 2, "week": 5, "winner": "home"}]

@app.post("/update-odds")
async def update_odds():
    """
    Automated trigger: Run sims (fetch schedule internally) and update Supabase.
    Expects POST body: {} (or any JSON, ignored)
    """
    try:
        # Run script, which fetches schedule itself (e.g., from Supabase Games table)
        results = simulate_odds({})  # Adjust if function expects specific args
        
        # Upsert into PlayoffOdds table
        data = {
            "league_id": "default",  # Hardcode since single league
            "playoff_odds": results,  # Must be JSON-serializable
            "updated_at": "now()"
        }
        response = supabase.table("PlayoffOdds").upsert(data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to update Supabase")
        
        return {"status": "success", "message": "Odds updated in Supabase"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-odds")
async def calculate_odds(request: ScheduleRequest):
    """
    User-specific: Run sims with provided schedule and return JSON.
    Expects POST body: {"incomplete_games": [...]}
    """
    try:
        # Run script with user-provided schedule
        results = simulate_odds(request.dict())  # Or run_tiebreakers(request.incomplete_games)
        return {"playoff_odds": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)