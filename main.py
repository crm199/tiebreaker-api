from fastapi import FastAPI
from supabase import create_client, Client
import os
from temp import run_tiebreakers  # your function
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.post("/run-tiebreakers")
def run_playoff_simulation():
    try:
        # Call your simulation function
        # It should read from Games, TeamRecords, etc., and write to PlayoffOdds
        run_tiebreakers(supabase)

        return {"status": "success", "message": "Playoff odds updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
