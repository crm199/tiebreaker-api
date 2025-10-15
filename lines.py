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

def round_half(x: float) -> float:
    """Round to nearest 0.5, always ending in .5"""
    x = round(x * 2) / 2.0
    if x == int(x):
        x += 0.5
    return x


def get_s2_ppp_data():
    """Read the S2 PPP Google Sheet into a DataFrame"""
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open(GOOGLE_SHEET_NAME).sheet1
    data = pd.DataFrame(sheet.get_all_records())

    # Normalize columns to consistent naming
    data = data.rename(columns={
        "Team": "Team",
        "oPPP": "oPPP",
        "dPPP": "dPPP",
        "O Poss / Game": "oPoss",
        "D Poss / Game": "dPoss"
    })

    # Add total possessions
    data["poss_per_game"] = data["oPoss"] + data["dPoss"]
    data.set_index("Team", inplace=True)
    return data


def get_s2_win_pcts(supabase_client):
    """Fetch win percentage from Supabase S2TeamRecords"""
    records = supabase_client.table(S2TEAMRECORDS_TABLE).select("Team, wins, losses").execute().data
    win_pcts = {}
    for rec in records:
        wins, losses = rec.get("wins", 0), rec.get("losses", 0)
        total = wins + losses
        win_pcts[rec["Team"]] = wins / total if total > 0 else 0.5
    return win_pcts


def weighted_merge_stats(team_stats, s2_ppp_df, s2_win_pcts, week_number):
    """Blend Season 1 and Season 2 stats by weighting"""
    s2_weight = min(0.05 * (week_number - 1), 1.0)  # Week 1 = 0%, Week 4 = 15%, max 100%
    s1_weight = 1 - s2_weight

    blended = {}
    for team_id, s1_data in team_stats.items():
        team_name = s1_data["Team"]
        if team_name not in s2_ppp_df.index:
            logger.warning(f"No S2 PPP data found for {team_name}, using S1 only.")
            blended[team_id] = s1_data
            continue

        s2_data = s2_ppp_df.loc[team_name]
        new_entry = s1_data.copy()

        # Weighted averages for oPPP, dPPP, and poss_per_game
        new_entry["oPPP"] = (s1_data["oPPP"] * s1_weight) + (s2_data["oPPP"] * s2_weight)
        new_entry["dPPP"] = (s1_data["dPPP"] * s1_weight) + (s2_data["dPPP"] * s2_weight)
        new_entry["poss_per_game"] = (s1_data["poss_per_game"] * s1_weight) + (s2_data["poss_per_game"] * s2_weight)

        # Replace win_pct with current one from Supabase if available
        if team_name in s2_win_pcts:
            new_entry["win_pct"] = s2_win_pcts[team_name]
        else:
            new_entry["win_pct"] = s1_data.get("win_pct", 0.5)

        blended[team_id] = new_entry

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

    # Adjust for possessions
    if team1_stats["poss_per_game"] <= 14:
        team1_stats["poss_per_game"] *= 0.99
    elif team1_stats["poss_per_game"] >= 15.5:
        team1_stats["poss_per_game"] *= 1.01

    if team2_stats["poss_per_game"] <= 14:
        team2_stats["poss_per_game"] *= 0.99
    elif team2_stats["poss_per_game"] >= 15.5:
        team2_stats["poss_per_game"] *= 1.01

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

    # Over/Under
    ou = round_half(team1_expected + team2_expected)

    # Spread
    pre_round_spread = (team1_expected - team2_expected) * 1.17
    spread = round_half(pre_round_spread)
    if spread > 9:
        add = (spread + 0.5 - 9) / 3
        spread += add

    # Win probability
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
    """Get all regular season games for a given week from Supabase and return predicted lines"""
    week_index = week_number - 1
    logger.info(f"Fetching games for week {week_number} (weekIndex={week_index})")

    # Step 1: Fetch season 2 live data
    s2_ppp_df = get_s2_ppp_data()
    s2_win_pcts = get_s2_win_pcts(supabase_client)

    # Step 2: Blend season 1 + season 2
    team_stats = weighted_merge_stats(team_stats, s2_ppp_df, s2_win_pcts, week_number)

    # Step 3: Get games
    response = supabase_client.table("Games").select("*") \
        .eq("weekIndex", week_index) \
        .eq("seasonIndex", SEASON_INDEX) \
        .eq("stageIndex", 1).execute()

    games = response.data
    logger.info(f"Retrieved {len(games)} games from Supabase")

    predictions = []

    for game in games:
        home_id = game["homeTeamId"]
        away_id = game["awayTeamId"]
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

    logger.info(f"Inserting {len(predictions)} predictions into WeeklyOdds")
    supabase_client.table("WeeklyOdds").insert(predictions).execute()

    print(f"✅ Updated WeeklyOdds for Week {week_number} using {int((1 - (0.05 * (week_number - 1))) * 100)}% Season 1 + {int(0.05 * (week_number - 1) * 100)}% Season 2 weighting")
    return predictions
