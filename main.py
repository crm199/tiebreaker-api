from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from tiebreakers import simulate_odds  # Import your script/module

app = FastAPI(title="Playoff Odds API")

# Supabase config (get these from your Supabase dashboard: Settings > API)
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-or-service-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic model for incoming schedule data (adjust fields to match your script's needs)
class ScheduleRequest(BaseModel):
    league_id: str  # Or whatever identifies the league
    incomplete_games: list[dict]  # e.g., [{"home_team": "DAL", "away_team": "PHI", "week": 5, ...}]
    # Add other fields like current standings if your script needs them

@app.post("/update-odds")
async def update_odds(request: ScheduleRequest):
    """
    Automated trigger: Run sims and update Supabase table.
    Expects POST body like: {"league_id": "abc123", "incomplete_games": [...]}
    """
    try:
        # Run your script with the provided schedule
        results = simulate_odds.run_simulations(request.dict())  # Adjust to match your function
        
        # Upsert into PlayoffOdds table (adjust table/columns as needed)
        data = {
            "league_id": request.league_id,
            "playoff_odds": results,  # Assuming results is JSON-serializable
            "updated_at": "now()"  # Or use datetime.utcnow()
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
    User-specific: Run sims with custom schedule and return JSON.
    Expects same POST body as above.
    """
    try:
        # Run your script with the provided (updated) schedule
        results = simulate_odds.run_simulations(request.dict())
        return {"playoff_odds": results}  # Just return the data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)