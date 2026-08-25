import logging
import math
import os
from collections import defaultdict
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import Client, create_client

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

LOGIT_COEF = 0.165
LOGIT_INTERCEPT = -0.0170

# WeeklyOdds stores a positive value when the HOME team is favored.
# The Discord bot displays 0.5 as: Home Team (-0.5).
DEFAULT_HOME_SPREAD = 0.5
DEFAULT_TOTAL = 60.5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# General helpers
# -------------------------------------------------------------------

def number(row: dict[str, Any], field: str) -> float:
    """Safely read a numeric database value."""
    return float(row.get(field) or 0)


def round_half(value: float) -> float:
    """Round to a half-point line, avoiding whole numbers."""
    value = round(value * 2) / 2.0
    return value + 0.5 if value == int(value) else value


def current_season_index(client: Client) -> int:
    """Find the newest scheduled season automatically."""
    rows = (
        client.table("Games")
        .select("seasonIndex")
        .order("seasonIndex", desc=True)
        .limit(1)
        .execute()
        .data
        or []
    )

    if not rows:
        raise RuntimeError("No Games rows found; cannot determine current season.")

    return int(rows[0]["seasonIndex"])


def season_weights(current_season: int, week_number: int) -> dict[int, float]:
    """
    Weight seasons dynamically.

    - Season 1: 100% Season 1.
    - Later seasons: current season gains 5% after each completed week,
      capped at 75%.
    - The immediately prior season gets 75% of the remaining weight,
      then the next-oldest gets 75% of what remains, etc.
    - Season 1 receives the final remaining weight.
    """
    if current_season < 0:
        raise ValueError("seasonIndex cannot be negative.")

    if current_season == 0:
        return {0: 1.0}

    # Lines are made before the requested week's games are played.
    # Week 1 therefore has 0% current-season data, Week 2 has 5%, etc.
    completed_weeks = max(week_number - 1, 0)
    current_weight = min(0.05 * completed_weeks, 0.75)

    weights = {current_season: current_weight}
    remaining = 1.0 - current_weight

    for season in range(current_season - 1, 0, -1):
        weight = remaining * 0.75
        weights[season] = weight
        remaining -= weight

    weights[0] = remaining
    return weights


# -------------------------------------------------------------------
# Supabase data loading
# -------------------------------------------------------------------

def fetch_team_names(client: Client) -> dict[int, str]:
    rows = client.table("Teams").select("teamId,displayName").execute().data or []

    return {
        int(row["teamId"]): row.get("displayName") or f"Team {row['teamId']}"
        for row in rows
    }


def fetch_season_stats(
    client: Client,
    season_index: int,
    through_week_index: int | None = None,
) -> dict[int, dict[str, float]]:
    """
    Build per-team season ratings from PPP and TeamRecords.

    Current-season data is limited to completed weeks. Historical seasons
    use their complete data.
    """
    ppp_query = (
        client.table("PPP")
        .select(
            "teamId,weekIndex,isSimmed,"
            "offPoss,defPoss,"
            "offTDs,offFGsMade,"
            "defTDs,defFGsMade"
        )
        .eq("seasonIndex", season_index)
    )

    if through_week_index is not None:
        ppp_query = ppp_query.lte("weekIndex", through_week_index)

    ppp_rows = ppp_query.execute().data or []

    totals: dict[int, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    for row in ppp_rows:
        # Simmed games should not influence the betting model.
        if row.get("isSimmed") is True:
            continue

        team_id = int(row["teamId"])

        for field in (
            "offPoss",
            "defPoss",
            "offTDs",
            "offFGsMade",
            "defTDs",
            "defFGsMade",
        ):
            totals[team_id][field] += number(row, field)

        totals[team_id]["games"] += 1

    stats: dict[int, dict[str, float]] = {}

    for team_id, total in totals.items():
        if total["offPoss"] <= 0 or total["defPoss"] <= 0:
            continue

        stats[team_id] = {
            "oPPP": (
                7 * total["offTDs"] + 3 * total["offFGsMade"]
            ) / total["offPoss"],
            "dPPP": (
                7 * total["defTDs"] + 3 * total["defFGsMade"]
            ) / total["defPoss"],
            # Average possessions for one team in a game.
            "poss_per_game": (
                total["offPoss"] + total["defPoss"]
            ) / (2 * total["games"]),
            "win_pct": 0.5,
            "avg_opp_ppp_diff": 0.0,
        }

    record_query = (
        client.table("TeamRecords")
        .select("teamId,wins,losses")
        .eq("seasonIndex", season_index)
    )

    records = record_query.execute().data or []

    for row in records:
        team_id = int(row["teamId"])

        if team_id not in stats:
            continue

        wins = number(row, "wins")
        losses = number(row, "losses")
        games = wins + losses

        stats[team_id]["win_pct"] = wins / games if games > 0 else 0.5

    game_query = (
        client.table("Games")
        .select("homeTeamId,awayTeamId,weekIndex")
        .eq("seasonIndex", season_index)
        .eq("stageIndex", 1)
    )

    if through_week_index is not None:
        game_query = game_query.lte("weekIndex", through_week_index)

    games = game_query.execute().data or []
    opponent_differentials: dict[int, list[float]] = defaultdict(list)

    for game in games:
        home_id = int(game["homeTeamId"])
        away_id = int(game["awayTeamId"])

        if home_id not in stats or away_id not in stats:
            continue

        home_net_ppp = stats[home_id]["oPPP"] - stats[home_id]["dPPP"]
        away_net_ppp = stats[away_id]["oPPP"] - stats[away_id]["dPPP"]

        opponent_differentials[home_id].append(away_net_ppp)
        opponent_differentials[away_id].append(home_net_ppp)

    for team_id, team_stats in stats.items():
        opponents = opponent_differentials[team_id]

        if opponents:
            team_stats["avg_opp_ppp_diff"] = sum(opponents) / len(opponents)

    return stats


def weighted_team_stats(
    client: Client,
    current_season: int,
    week_number: int,
) -> dict[int, dict[str, float]]:
    """Blend every available season into one current team rating."""
    weights = season_weights(current_season, week_number)

    all_season_stats: dict[int, dict[int, dict[str, float]]] = {}

    for season_index in weights:
        # Only current-season ratings need to exclude the requested week.
        through_week = week_number - 2 if season_index == current_season else None

        all_season_stats[season_index] = fetch_season_stats(
            client,
            season_index,
            through_week_index=through_week,
        )

    team_ids = set()

    for stats in all_season_stats.values():
        team_ids.update(stats.keys())

    fields = (
        "oPPP",
        "dPPP",
        "poss_per_game",
        "win_pct",
        "avg_opp_ppp_diff",
    )

    blended: dict[int, dict[str, float]] = {}

    for team_id in team_ids:
        available = [
            (season, all_season_stats[season][team_id])
            for season in weights
            if team_id in all_season_stats[season] and weights[season] > 0
        ]

        # A team with no usable data in any season will receive the
        # standard -0.5 / 60.5 fallback when its game is generated.
        if not available:
            continue

        total_weight = sum(weights[season] for season, _ in available)

        blended[team_id] = {
            field: sum(
                weights[season] * stats[field]
                for season, stats in available
            ) / total_weight
            for field in fields
        }

    logger.info(
        "Season weights for Week %s: %s",
        week_number,
        {
            f"Season {season + 1}": f"{weight:.1%}"
            for season, weight in sorted(weights.items())
        },
    )

    return blended


# -------------------------------------------------------------------
# Line calculation
# -------------------------------------------------------------------

def calculate_lines(
    home_stats: dict[str, float],
    away_stats: dict[str, float],
) -> dict[str, float]:
    """Calculate the spread, total, expected scores, and home win chance."""
    home = home_stats.copy()
    away = away_stats.copy()

    for stats in (home, away):
        win_pct_weight = ((stats["win_pct"] - 0.5) + 35) / 35
        sos_weight = max(0.5, (stats["avg_opp_ppp_diff"] + 60) / 60)

        stats["oPPP"] *= win_pct_weight * sos_weight
        stats["dPPP"] /= win_pct_weight * sos_weight

        if stats["poss_per_game"] <= 14:
            stats["poss_per_game"] *= 0.99
        elif stats["poss_per_game"] >= 15.5:
            stats["poss_per_game"] *= 1.02

    average_possessions = (
        home["poss_per_game"] + away["poss_per_game"]
    ) / 2

    home_expected = (
        (home["oPPP"] + away["dPPP"]) / 2
    ) * average_possessions

    away_expected = (
        (away["oPPP"] + home["dPPP"]) / 2
    ) * average_possessions

    if home["poss_per_game"] > 15.5 and away["poss_per_game"] > 15.5:
        home_expected *= 1.02
        away_expected *= 1.02

    if home["oPPP"] > 4 and away["oPPP"] > 4:
        home_expected *= 1.03
        away_expected *= 1.03
    elif home["oPPP"] > 4 and away["oPPP"] < 3.3:
        away_expected *= 0.985
    elif home["oPPP"] < 3.3 and away["oPPP"] > 4:
        home_expected *= 0.985

    total = home_expected + away_expected

    if total > 54:
        total += (total + 0.5 - 54) / 2.1

    pre_round_spread = (home_expected - away_expected) * 1.25
    spread = pre_round_spread

    if spread > 6.5:
        spread += (spread + 0.5 - 6.5) / 2.2
    elif spread > 2.5:
        spread += (spread + 0.5 - 2.5) / 3.3

    home_win_probability = 1 / (
        1 + math.exp(-(LOGIT_COEF * pre_round_spread + LOGIT_INTERCEPT))
    )

    return {
        "spread": round_half(spread),
        "ou": round_half(total),
        "homeExpectedScore": home_expected,
        "awayExpectedScore": away_expected,
        "winProbHome": home_win_probability,
    }


def default_line() -> dict[str, float]:
    """Use this whenever either team has no usable historical PPP data."""
    return {
        "spread": DEFAULT_HOME_SPREAD,
        "ou": DEFAULT_TOTAL,
        "homeExpectedScore": 30.5,
        "awayExpectedScore": 30.0,
        "winProbHome": 0.5,
    }


# -------------------------------------------------------------------
# Weekly generation and API endpoint
# -------------------------------------------------------------------

def predict_week_games(
    week_number: int,
    supabase_client: Client,
    season_index: int | None = None,
) -> list[dict[str, Any]]:
    """Create or update WeeklyOdds for the requested week."""
    current_season = (
        current_season_index(supabase_client)
        if season_index is None
        else season_index
    )

    week_index = week_number - 1

    ratings = weighted_team_stats(
        supabase_client,
        current_season,
        week_number,
    )

    names = fetch_team_names(supabase_client)

    games = (
        supabase_client.table("Games")
        .select("scheduleId,homeTeamId,awayTeamId")
        .eq("seasonIndex", current_season)
        .eq("weekIndex", week_index)
        .eq("stageIndex", 1)
        .execute()
        .data
        or []
    )

    predictions: list[dict[str, Any]] = []

    for game in games:
        home_id = int(game["homeTeamId"])
        away_id = int(game["awayTeamId"])

        # If either team has no usable data, use the standard line.
        if home_id not in ratings or away_id not in ratings:
            line = default_line()
            logger.info(
                "Using default line for %s at %s because one or both teams lack data.",
                names.get(away_id, away_id),
                names.get(home_id, home_id),
            )
        else:
            line = calculate_lines(ratings[home_id], ratings[away_id])

        predictions.append(
            {
                "scheduleId": game["scheduleId"],
                "seasonIndex": current_season,
                "weekIndex": week_index,
                "homeTeam": names.get(home_id, f"Team {home_id}"),
                "awayTeam": names.get(away_id, f"Team {away_id}"),
                "simmed": False,
                "closed": False,
                **line,
            }
        )

    if predictions:
        (
            supabase_client.table("WeeklyOdds")
            .upsert(predictions, on_conflict="scheduleId,seasonIndex")
            .execute()
        )

    logger.info(
        "Generated %s lines for Season %s, Week %s.",
        len(predictions),
        current_season + 1,
        week_number,
    )

    return predictions