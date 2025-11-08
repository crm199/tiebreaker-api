import logging
import pandas as pd
from supabase import create_client, Client
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from tiebreakers import playoffPercentages, simulate_odds
from lines import predict_week_games
import traceback

TEAMS_CSV = "TeamIDMap.csv"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/tmp/app.log"),
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

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#logger.info(f"SUPABASE_URL: {SUPABASE_URL}")
#logger.info(f"SUPABASE_KEY: {'[REDACTED]' if SUPABASE_KEY else None}")
if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Missing SUPABASE_URL or SUPABASE_KEY")
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY")

# FastAPI app
app = FastAPI()
logger.info("FastAPI app initialized")

# Add CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # Explicitly allow POST and OPTIONS
    allow_headers=["Content-Type", "Accept"],  # Allow relevant headers
)
# Request model
class ScheduleRequest(BaseModel):
    incomplete_games: list[dict]

class WeekRequest(BaseModel):
    week_number: int

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
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-odds")
async def calculate_odds(request: Request):
    logger.info("POST /calculate-odds called")
    try:
        # Get raw JSON data from the request
        json_data = await request.json()
        logger.info(f"Received JSON data: {json_data}")
        
        # Pass the JSON data directly to simulate_odds
        results = simulate_odds(json_data)
        logger.info("simulate_odds ran successfully")
        return {"status": "success", "playoff_odds": results}
    except Exception as e:
        logger.error(f"Error in /calculate-odds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/predict-lines")
async def predict_lines(week_req: WeekRequest):
    logger.info(f"POST /predict-lines called for week {week_req.week_number}")
    try:
        team_df = pd.read_csv("TeamIDMap.csv")
        team_stats = {
            row["ID"]: {
                "Team": row["Team"],
                "oPPP": row["oPPP"],
                "dPPP": row["dPPP"],
                "poss_per_game": row["poss_per_game"],
                "win_pct": row["win_pct"],
                "avg_opp_ppp_diff": row["avg_opp_ppp_diff"]
            }
            for _, row in team_df.iterrows()
        }
        logger.info(f"Loaded team stats for {len(team_stats)} teams")
        predictions = predict_week_games(week_req.week_number, team_stats, supabase)
        logger.info(f"Predictions generated for week {week_req.week_number}")
        return {"status": "success", "predictions": predictions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

