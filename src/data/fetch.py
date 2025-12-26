import requests
import json
from pathlib import Path
from src.config import ENDPOINTS

RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_and_save(name, url):
    response = requests.get(url)
    response.raise_for_status()

    filepath = RAW_DATA_DIR / f"{name}.json"
    with open(filepath, "w") as f:
        json.dump(response.json(), f)

    return filepath

def fetch_bootstrap():
    return fetch_and_save("bootstrap", ENDPOINTS["bootstrap"])

def fetch_fixtures():
    return fetch_and_save("fixtures", ENDPOINTS["fixtures"])

def fetch_player_history(player_id: int):
    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    return fetch_and_save(f"player_{player_id}", url)

