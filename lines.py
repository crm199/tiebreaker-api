import numpy as np
import pandas as pd
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- CONFIG ----------------
SEASON_INDEX = 1  # current season
LOGIT_COEF = 0.2254
LOGIT_INTERCEPT = -0.0170
GOOGLE_SHEET_NAME = "S2 PPP"
S2TEAMRECORDS_TABLE = "S2TeamRecords"
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
    """Read the S2 PPP Google Sheet into a DataFrame"""
    logger.info("Attempting to connect to Google Sheets...")
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        logger.info("Successfully authorized Google service account.")
    except Exception as e:
        logger.exception(f"Failed during Google Sheets authorization: {e}")
        raise

    try:
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        data = pd.DataFrame(sheet.get_all_records())
        logger.info(f"Retrieved {len(data)} rows from sheet '{GOOGLE_SHEET_NAME}'")
    except Exception as e:
        logger.exception(f"Error retrieving or parsing Google Sheet '{GOOGLE_SHEET_NAME}': {e}")
        raise

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
        records = supabase_client.table(S2TEAMRECORDS_TABLE).select("Team, wins, losses").execute().data
        logger.info(f"Retrieved {len(records)} records from S2TeamRecords.")
    except Exception as e:
        logger.exception(f"Supabase query failed when fetching S2TeamRecords: {e}")
        raise

    win_pcts = {}
    for rec in records:
        team = rec.get("Team")
        if not team:
            logger.warning(f"Skipping record with no Team field: {rec}")
            continue
        wins, losses = rec.get("wins", 0), rec.get("losses", 0)
        total = wins + losses
        win_pcts[team] = wins / total if total > 0 else 0.5

    logger.debug(f"Computed win_pcts for {len(win_pcts)} teams.")
    return win_pcts


def weighted_merge_stats(team_stats, s2_ppp_df, s2_win_pcts, week_number):
    """Blend Season 1 and Season 2 stats by weighting"""
    s2_weight = min(0.05 * (week_number - 1), 1.0)  # 5% more S2 per week
    s1_weight = 1 - s2_weight
    logger.info(f"Blending stats with weights: {s1_weight:.2f} S1 | {s2_weight:.2f} S2")

    blended = {}
    for team_id, s1_data in team_stats.items():
        team_name = s1_data["Team"]

        if team_name not in s2_ppp_df.index:
            logger.warning(f"No S2 PPP data found for {team_name}, using only S1 values.")
            blended[team_id] = s1_data
            continue

        try:
            s2_data = s2_ppp_df.loc[team_name]
            new_entry = s1_data.copy()

            new_entry["oPPP"] = (s1_data["oPPP"] * s1_weight) + (s2_data["oPPP"] * s2_weight)
            new_entry["dPPP"] = (s1_data["dPPP"] * s1_weight) + (s2_data["dPPP"] * s2_weight)
            new_entry["poss_per_game"] = (s1_data["poss_per_game"] * s1_weight) + (s2_data["poss_per_game"] * s2_weight)
            new_entry["win_pct"] = s2_win_pcts.get(team_name, s1_data.get("win_pct", 0.5))
            blended[team_id] = new_entry
        except Exception as e:
            logger.exception(f"Error blending data for {team_name}: {e}")
            blended[team_id] = s1_data

    logger.info(f"Blended data for {len(blended)} teams.")
    return blended


def lines(team1_stats: dict, team2_stats: dict):
    """Compute expected scores, spread, O/U, and pre-round spread"""
    logger.debug(f"Calculating line for {team1_stats.get('Team')} vs {team2_stats.get('Team')}")

    # Apply weights
    team1_stats["win_pct_weight"] = ((team1_stats["win_pct"] - 0.5) + 35) / 35
    team2_stats["win_pct_weight"] = ((team2_stats["win_pct"] - 0.5) + 35) / 35

    team1_stats["sos_weight"] = ((team1_stats["avg_opp_ppp_diff"] + 35) / 35)
    team2_stats["sos_weight"] = ((team2_stats["avg_opp_ppp_diff"] + 35) / 35)

    team1_stats["oPPP"] *= team1_stats["win_pct_weight"] * team1_stats["sos_weight"]
    team1_stats["dPPP"] /= team1_stats["win_pct_weight"] * team1_stats["sos_weight"]
    team2_stats["oPPP"] *= team2_stats["win_pct_weight"] * team2_stats["sos_weight"]
    team2_stats["dPPP"] /= team2_stats["win_pct_weight"] * team2_stats["sos_weight"]

    # Possession adjustments
    for team, stats in [("home", team1_stats), ("away", team2_stats)]:
        if stats["poss_per_game"] <= 14:
            stats["poss_per_game"] *= 0.99
        elif stats["poss_per_game"] >= 15.5:
            stats["poss_per_game"] *= 1.01

    # Expected scores
    team1_expected = (team1_stats["oPPP"] + team2_stats["dPPP"]) / 2 * (
        (team1_stats["poss_per_game"] + team2_stats["poss_per_game"]) / 4
    )
    team2_expected = (team2_stats["oPPP"] + team1_stats["dPPP"]) / 2 * (
        (team1_stats["poss_per_game"] + team2_stats["poss_per_game"]) / 4
    )

    if (team1_stats["poss_per_game"] > 15.5) and (team2_stats["poss_per_game"] > 15.5):
        team1_expected *= 1.02
        team2_expected *= 1.02
    elif (team1_stats["poss_per_game"] < 14) and (team2_stats["poss_per_game"] < 14):
        team1_expected *= 0.98
        team2_expected *= 0.98

    ou = round_half(team1_expected + team2_expected)
    pre_round_spread = (team1_expected - team2_expected) * 1.17
    spread = round_half(pre_round_spread)
    if spread > 9:
        spread += (spread + 0.5 - 9) / 3

    win_prob_home = 1 / (1 + np.exp(-(LOGIT_COEF * pre_round_spread + LOGIT_INTERCEPT)))

    return {
        "homeExpectedScore": team1_expected,
        "awayExpectedScore": team2_expected,
        "spread": spread,
        "ou": ou,
        "winProbHome": win_prob_home,
        "pre_round_spread": pre_round_spread,
    }


def predict_week_games(week_number: int, team_stats: dict, supabase_client) -> list[dict]:
    """Main entry: predict all games for a week"""
    logger.info(f"=== Predicting week {week_number} ===")
    week_index = week_number - 1

    try:
        s2_ppp_df = get_s2_ppp_data()
        s2_win_pcts = get_s2_win_pcts(supabase_client)
        logger.info("Loaded both S2 PPP data and win_pcts successfully.")
    except Exception as e:
        logger.exception(f"Failed during S2 data loading: {e}")
        raise

    try:
        team_stats = weighted_merge_stats(team_stats, s2_ppp_df, s2_win_pcts, week_number)
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

    print(f"✅ Updated WeeklyOdds for Week {week_number} ({int((1 - (0.05 * (week_number - 1))) * 100)}% S1 + {int(0.05 * (week_number - 1) * 100)}% S2 weighting)")
    return predictions
