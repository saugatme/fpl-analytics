import json
import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def process_players():
    with open(RAW_DATA_DIR / "bootstrap.json") as f:
        data = json.load(f)

    players = pd.DataFrame(data["elements"])
    teams = pd.DataFrame(data["teams"])[["id", "name"]]

    players = players.merge(
        teams,
        left_on="team",
        right_on="id",
        suffixes=("", "_team")
    )

    players = players[
        [
            "id",
            "first_name",
            "second_name",
            "element_type",
            "now_cost",
            "minutes",
            "total_points",
        ]
    ]

    players.to_csv(PROCESSED_DATA_DIR / "players.csv", index=False)
    return players

def process_fixtures():
    with open(RAW_DATA_DIR / "fixtures.json") as f:
        data = json.load(f)

    fixtures = pd.DataFrame(data)

    fixtures = fixtures[
        [
            "id",
            "event",
            "team_h",
            "team_a",
            "team_h_difficulty",
            "team_a_difficulty",
            "kickoff_time"
        ]
    ]

    fixtures.to_csv(PROCESSED_DATA_DIR / "fixtures.csv", index=False)
    return fixtures

def process_player_history(player_id: int):
    path = RAW_DATA_DIR / f"player_{player_id}.json"

    if not path.exists():
        return None

    with open(path) as f:
        data = json.load(f)

    history = pd.DataFrame(data["history"])
    history["player_id"] = player_id
    return history

def process_all_player_histories(player_ids):
    dfs = []

    for pid in player_ids:
        df = process_player_history(pid)
        if df is not None:
            dfs.append(df)

    if not dfs:
        return None

    all_history = pd.concat(dfs, ignore_index=True)
    all_history.to_csv(PROCESSED_DATA_DIR / "player_gameweek.csv", index=False)
    return all_history
