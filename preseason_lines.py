import csv

from lines import (
    supabase,
    weighted_team_stats,
    fetch_team_names,
    calculate_lines,
    default_line,
    logger,
)

SEASON_INDEX = 1          # Season 2 (the season you're predicting)
OUTPUT_FILE = "season_2_preseason_lines.csv"


def generate_full_season_lines() -> list[dict]:
    # Week 1 weights = 0% current season, 100% prior season(s), so this
    # uses only Season 1 data for every game in the season.
    ratings = weighted_team_stats(supabase, SEASON_INDEX, week_number=1)
    names = fetch_team_names(supabase)

    games = (
        supabase.table("Games")
        .select("scheduleId,homeTeamId,awayTeamId,weekIndex")
        .eq("seasonIndex", SEASON_INDEX)
        .eq("stageIndex", 1)
        .order("weekIndex")
        .execute()
        .data
        or []
    )

    rows = []

    for game in games:
        home_id = int(game["homeTeamId"])
        away_id = int(game["awayTeamId"])

        if home_id not in ratings or away_id not in ratings:
            line = default_line()
            logger.info(
                "Using default line for %s at %s (missing data).",
                names.get(away_id, away_id),
                names.get(home_id, home_id),
            )
        else:
            line = calculate_lines(ratings[home_id], ratings[away_id])

        rows.append(
            {
                "scheduleId": game["scheduleId"],
                "seasonIndex": SEASON_INDEX,
                "weekIndex": game["weekIndex"],
                "week": int(game["weekIndex"]) + 1,
                "homeTeam": names.get(home_id, f"Team {home_id}"),
                "awayTeam": names.get(away_id, f"Team {away_id}"),
                **line,
            }
        )

    return rows


if __name__ == "__main__":
    rows = generate_full_season_lines()

    if not rows:
        raise SystemExit("No games found for that season/stage.")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} games to {OUTPUT_FILE}")