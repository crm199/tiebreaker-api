import numpy as np
import pandas as pd
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import base64

# ---------------- CONFIG ----------------
SEASON_INDEX = 2  # current season
LOGIT_COEF = 0.165
LOGIT_INTERCEPT = -0.0170
GOOGLE_SHEET_NAME = "MML26 Run-Pass and PPP Tracker"  # <-- spreadsheet name
RP_TRACKER_SHEET_NAME = "S2 PPP"
RP_TRACKER_SHEET_NAME_S3 = "S3 PPP"
S2TEAMRECORDS_TABLE = "S2TeamRecords"
S3TEAMRECORDS_TABLE = "S3TeamRecords"
# ---------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)


def round_half(x: float) -> float:
    """Round to nearest 0.5, always ending in .5"""
    x = round(x * 2) / 2.0
    if x == int(x):
        x += 0.5
    return x


def get_s2_ppp_data():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds_b64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_B64")
    if not creds_b64:
        raise ValueError("Missing GOOGLE_SERVICE_ACCOUNT_B64 environment variable")

    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).worksheet(RP_TRACKER_SHEET_NAME)
    data = pd.DataFrame(sheet.get_all_records())

    logger.debug(f"Sheet columns: {list(data.columns)}")

    try:
        # Normalize columns
        data = data.rename(columns={
            "Team": "Team",
            "oPPP": "oPPP",
            "dPPP": "dPPP",
            "O Poss / Game": "oPoss",
            "D Poss / Game": "dPoss"
        })

        if not all(col in data.columns for col in ["Team", "oPPP", "dPPP", "oPoss", "dPoss"]):
            logger.error("Missing one or more required columns in Google Sheet data!")
            raise KeyError(f"Columns found: {data.columns}")

        data["poss_per_game"] = data["oPoss"] + data["dPoss"]
        data.set_index("Team", inplace=True)
    except Exception as e:
        logger.exception(f"Error processing Google Sheet data: {e}")
        raise

    logger.info("Successfully loaded S2 PPP data from Google Sheets.")
    return data

def get_s3_ppp_data():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds_b64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_B64")
    if not creds_b64:
        raise ValueError("Missing GOOGLE_SERVICE_ACCOUNT_B64 environment variable")

    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).worksheet(RP_TRACKER_SHEET_NAME_S3)
    data = pd.DataFrame(sheet.get_all_records())

    logger.debug(f"Sheet columns: {list(data.columns)}")

    try:
        # Normalize columns
        data = data.rename(columns={
            "Team": "Team",
            "oPPP": "oPPP",
            "dPPP": "dPPP",
            "O Poss / Game": "oPoss",
            "D Poss / Game": "dPoss"
        })

        if not all(col in data.columns for col in ["Team", "oPPP", "dPPP", "oPoss", "dPoss"]):
            logger.error("Missing one or more required columns in Google Sheet data!")
            raise KeyError(f"Columns found: {data.columns}")

        data["poss_per_game"] = data["oPoss"] + data["dPoss"]
        data.set_index("Team", inplace=True)
    except Exception as e:
        logger.exception(f"Error processing Google Sheet data: {e}")
        raise

    logger.info("Successfully loaded S2 PPP data from Google Sheets.")
    return data



def get_s2_win_pcts(supabase_client):
    """Fetch win percentage from Supabase S2TeamRecords"""
    logger.info("Fetching Season 2 win percentages from Supabase...")
    try:
        records = supabase_client.table(S2TEAMRECORDS_TABLE).select("teamId, wins, losses").execute().data
        logger.info(f"Retrieved {len(records)} records from S2TeamRecords.")
    except Exception as e:
        logger.exception(f"Supabase query failed when fetching S2TeamRecords: {e}")
        raise

    win_pcts = {}
    for rec in records:
        team_id = rec.get("teamId")
        if not team_id:
            logger.warning(f"Skipping record with no teamId field: {rec}")
            continue
        wins, losses = rec.get("wins", 0), rec.get("losses", 0)
        total = wins + losses
        win_pcts[team_id] = wins / total if total > 0 else 0.5

    logger.debug(f"Computed win_pcts for {len(win_pcts)} teams.")
    return win_pcts

def get_s3_win_pcts(supabase_client):
    """Fetch win percentage from Supabase S2TeamRecords"""
    logger.info("Fetching Season 2 win percentages from Supabase...")
    try:
        records = supabase_client.table(S3TEAMRECORDS_TABLE).select("teamId, wins, losses").execute().data
        logger.info(f"Retrieved {len(records)} records from S2TeamRecords.")
    except Exception as e:
        logger.exception(f"Supabase query failed when fetching S2TeamRecords: {e}")
        raise

    win_pcts = {}
    for rec in records:
        team_id = rec.get("teamId")
        if not team_id:
            logger.warning(f"Skipping record with no teamId field: {rec}")
            continue
        wins, losses = rec.get("wins", 0), rec.get("losses", 0)
        total = wins + losses
        win_pcts[team_id] = wins / total if total > 0 else 0.5

    logger.debug(f"Computed win_pcts for {len(win_pcts)} teams.")
    return win_pcts


def weighted_merge_stats(team_stats, s2_ppp_df, s3_ppp_df, s2_win_pcts, s3_win_pcts, week_number):
    # Season 3 gains +5% every week
    s3_weight = max(0, min(0.05 * (week_number - 1), 0.80))  # capped at 80%

    # Remaining weight split 1:4 between S1 and S2
    remaining = 1 - s3_weight
    s1_weight = remaining * (0.2)   # 20% of remaining
    s2_weight = remaining * (0.8)   # 80% of remaining

    logger.info(f"Blending weights: S1={s1_weight:.2%} | S2={s2_weight:.2%} | S3={s3_weight:.2%}")

    blended = {}
    for team_id, s1_data in team_stats.items():
        lookup_key = team_id if team_id in s2_ppp_df.index else s1_data.get("Team")

        if lookup_key not in s2_ppp_df.index:
            logger.warning(f"No S2 PPP data found for {lookup_key}, using only S1 values.")
            blended[team_id] = s1_data
            continue

        try:
            s2_data = s2_ppp_df.loc[lookup_key]
            new_entry = s1_data.copy()
            s3_data = s3_ppp_df.loc[lookup_key]

            new_entry["oPPP"] = (
                s1_data["oPPP"] * s1_weight +
                s2_data["oPPP"] * s2_weight +
                s3_data["oPPP"] * s3_weight
            )

            new_entry["dPPP"] = (
                s1_data["dPPP"] * s1_weight +
                s2_data["dPPP"] * s2_weight +
                s3_data["dPPP"] * s3_weight
            )

            new_entry["poss_per_game"] = (
                s1_data["poss_per_game"] * s1_weight +
                s2_data["poss_per_game"] * s2_weight +
                s3_data["poss_per_game"] * s3_weight
            )

            s1_win = s1_data.get("win_pct", 0.5)
            s2_win = s2_win_pcts.get(team_id, 0.5)
            s3_win = s3_win_pcts.get(team_id, 0.5)

            new_entry["win_pct"] = (
                s1_win * s1_weight +
                s2_win * s2_weight +
                s3_win * s3_weight
            )

            blended[team_id] = new_entry
        except Exception as e:
            logger.exception(f"Error blending data for {lookup_key}: {e}")
            blended[team_id] = s1_data

    logger.info(f"Blended data for {len(blended)} teams.")
    return blended


def lines(team1_stats: dict, team2_stats: dict):
    """Compute expected scores, spread, O/U, and pre-round spread"""
    t1 = team1_stats.copy()
    t2 = team2_stats.copy()

    # WIN % + SOS adjustments
    t1["win_pct_weight"] = ((t1["win_pct"] - 0.5) + 35) / 35
    t2["win_pct_weight"] = ((t2["win_pct"] - 0.5) + 35) / 35

    t1["sos_weight"] = ((t1["avg_opp_ppp_diff"] + 60) / 60)
    t2["sos_weight"] = ((t2["avg_opp_ppp_diff"] + 60) / 60)

    t1["oPPP"] *= t1["win_pct_weight"] * t1["sos_weight"]
    t1["dPPP"] /= t1["win_pct_weight"] * t1["sos_weight"]

    t2["oPPP"] *= t2["win_pct_weight"] * t2["sos_weight"]
    t2["dPPP"] /= t2["win_pct_weight"] * t2["sos_weight"]

    # Possession scaling
    for stats in [t1, t2]:
        if stats["poss_per_game"] <= 14:
            stats["poss_per_game"] *= 0.99
        elif stats["poss_per_game"] >= 15.5:
            stats["poss_per_game"] *= 1.02

    # Expected scores
    t1_exp = (t1["oPPP"] + t2["dPPP"]) / 2 * ((t1["poss_per_game"] + t2["poss_per_game"]) / 4)
    t2_exp = (t2["oPPP"] + t1["dPPP"]) / 2 * ((t1["poss_per_game"] + t2["poss_per_game"]) / 4)

    if (t1["poss_per_game"] > 15.5 and t2["poss_per_game"] > 15.5):
        t1_exp *= 1.02
        t2_exp *= 1.02

    if t1["oPPP"] > 4 and t2["oPPP"] > 4:
        t1_exp *= 1.03
        t2_exp *= 1.03
    elif t1["oPPP"] > 4 and t2["oPPP"] < 3.3:
        t2_exp *= 0.985
    elif t1["oPPP"] < 3.3 and t2["oPPP"] > 4:
        t1_exp *= 0.985

    ou = (t1_exp + t2_exp)
    if ou > 54:
        ou += (ou + 0.5 - 54) / 2.1
    ou = round_half(ou)

    pre_round_spread = (t1_exp - t2_exp) * 1.25
    #spread = round_half(pre_round_spread)
    spread = pre_round_spread
    if spread > 6.5:
        spread += (spread + 0.5 - 6.5) / 2.2
    elif spread > 2.5:
        spread += (spread + 0.5 - 2.5) / 3.3
    spread = round_half(spread)

    # NEW WIN PROBABILITY (flatter logistic)
    win_prob_home = 1 / (1 + np.exp(-(LOGIT_COEF * pre_round_spread + LOGIT_INTERCEPT)))

    return {
        "spread": spread,
        "ou": ou,
        "homeExpectedScore": t1_exp,
        "awayExpectedScore": t2_exp,
        "winProbHome": win_prob_home,
        "pre_round_spread": pre_round_spread,
    }


def predict_week_games(week_number: int, team_stats: dict, supabase_client) -> list[dict]:
    """Main entry: predict all games for a week"""
    logger.info(f"=== Predicting week {week_number} ===")
    week_index = week_number - 1

    try:
        s2_ppp_df = get_s2_ppp_data()
        s3_ppp_df = get_s3_ppp_data()
        s2_win_pcts = get_s2_win_pcts(supabase_client)
        s3_win_pcts = get_s3_win_pcts(supabase_client)
        logger.info("Loaded both S2 PPP data and win_pcts successfully.")
    except Exception as e:
        logger.exception(f"Failed during S2 data loading: {e}")
        raise

    try:
        team_stats = weighted_merge_stats(team_stats, s2_ppp_df, s3_ppp_df, s2_win_pcts, s3_win_pcts, week_number)
    except Exception as e:
        logger.exception(f"Error blending season stats: {e}")
        raise

    try:
        response = (
            supabase_client.table("Games")
            .select("*")
            .eq("weekIndex", week_index)
            .eq("seasonIndex", SEASON_INDEX)
            .eq("stageIndex", 1)
            .execute()
        )
        games = response.data
        logger.info(f"Retrieved {len(games)} games from Supabase for weekIndex={week_index}")
    except Exception as e:
        logger.exception(f"Supabase query failed for Games table: {e}")
        raise

    predictions = []
    for game in games:
        try:
            home_id, away_id = game["homeTeamId"], game["awayTeamId"]
            home_stats = team_stats[home_id]
            away_stats = team_stats[away_id]
            result = lines(home_stats, away_stats)

            predictions.append({
                "homeTeam": home_stats["Team"],
                "awayTeam": away_stats["Team"],
                "homeExpScore": result["homeExpectedScore"],
                "awayExpScore": result["awayExpectedScore"],
                "scheduleId": game["scheduleId"],
                "spread": result["spread"],
                "ou": result["ou"],
                "winProbHome": result["winProbHome"],
                "simmed": False,
                "weekIndex": week_index,
                "closed": False,
            })
        except Exception as e:
            logger.exception(f"Error processing game {game}: {e}")

    try:
        logger.info(f"Inserting {len(predictions)} predictions into WeeklyOdds...")
        supabase_client.table("WeeklyOdds").insert(predictions).execute()
        logger.info("✅ Successfully inserted predictions into WeeklyOdds.")
    except Exception as e:
        logger.exception(f"Error inserting predictions into WeeklyOdds: {e}")
        raise

    print(
        f"✅ Updated WeeklyOdds for Week {week_number} "
    )
    return predictions
