import json
import os

CACHE_FILE = "data/market_scan_cache.json"


def load_market_scan_cache():
    if not os.path.exists(CACHE_FILE):
        return {
            "updated_at": "",
            "progress": {
                "processed": 0,
                "total": 0,
                "last_symbol": "-"
            },
            "suitable": [],
            "buy": [],
            "hold": [],
            "sell": [],
            "failed": []
        }

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "progress" not in data:
            data["progress"] = {
                "processed": 0,
                "total": 0,
                "last_symbol": "-"
            }

        return data
    except Exception:
        return {
            "updated_at": "",
            "progress": {
                "processed": 0,
                "total": 0,
                "last_symbol": "-"
            },
            "suitable": [],
            "buy": [],
            "hold": [],
            "sell": [],
            "failed": []
        }


def save_market_scan_cache(data):
    os.makedirs("data", exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)