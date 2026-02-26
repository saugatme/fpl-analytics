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

