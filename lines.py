import numpy as np
import pandas as pd
import logging

# ---------------- CONFIG ----------------
SEASON_INDEX = 0  # default season index
LOGIT_COEF = 0.2254
LOGIT_INTERCEPT = -0.0170
# ---------------------------------------

logger = logging.getLogger(__name__)

def round_half(x: float) -> float:
    """Round to nearest 0.5, always ending in .5"""
    x = round(x * 2) / 2.0
    if x == int(x):
        x += 0.5
    return x

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

    # Win probability for home team using pre-trained logistic regression
    win_prob_home = 1 / (1 + np.exp(-(LOGIT_COEF * pre_round_spread + LOGIT_INTERCEPT)))

    logger.debug(
        f"Result: homeExp={team1_expected:.2f}, awayExp={team2_expected:.2f}, "
        f"spread={spread}, ou={ou}, winProbHome={win_prob_home:.3f}"
    )

    return {
        "homeExpectedScore": team1_expected,
        "awayExpectedScore": team2_expected,
        "spread": spread,
        "ou": ou,
        "winProbHome": win_prob_home,
        "pre_round_spread": pre_round_spread,
    }

def predict_week_games(week_number: int, team_stats: dict, supabase_client) -> list[dict]:
    """
    Get all regular season games for a given week from Supabase and return predicted lines
    """
    week_index = week_number - 1
    logger.info(f"Fetching games for week {week_number} (weekIndex={week_index})")

    response = supabase_client.table("Games").select("*") \
        .eq("weekIndex", week_index) \
        .eq("seasonIndex", SEASON_INDEX) \
        .eq("stageIndex", 1).execute()
    logger.info(f"Supabase query response: {response}")

    #if response.error:
    #    logger.error(f"Supabase query failed: {response.error}")
    #    raise Exception(f"Supabase query failed: {response.error}")
    
    logger.info("We got here")
    
    games = response.data
    logger.info(f"Retrieved {len(games)} games from Supabase")

    predictions = []

    for game in games:
        home_id = game["homeTeamId"]
        away_id = game["awayTeamId"]
        logger.debug(f"Predicting for Game {game.get('scheduleId')} | Home={home_id}, Away={away_id}")

        home_stats = team_stats[home_id]
        away_stats = team_stats[away_id]

        result = lines(home_stats, away_stats)

        pred = {
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
        }
        predictions.append(pred)

    logger.info(f"Generated {len(predictions)} predictions. Inserting into WeeklyOdds...")
    logger.info(f"Predctions: {predictions}")

    insert_resp = supabase_client.table("WeeklyOdds").insert(predictions).execute()
    if insert_resp.error:
        logger.error(f"Supabase insert failed: {insert_resp.error}")
        raise Exception(f"Supabase insert failed: {insert_resp.error}")

    logger.info("Insert into WeeklyOdds completed successfully")
    return predictions
