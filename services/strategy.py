from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from services.market_scan import load_market_scan

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DAILY_STRATEGY_FILE = CACHE_DIR / "daily_strategy.json"


def _score_item(item: dict[str, Any]) -> float:
    score = 0.0

    signal = item.get("signal", "")
    price = float(item.get("price", 0) or 0)
    ma20 = float(item.get("ma20", 0) or 0)
    fair_value = float(item.get("fair_value", 0) or 0)

    if signal == "BUY":
        score += 50
    elif signal == "HOLD":
        score += 20
    elif signal == "SELL":
        score -= 30

    if ma20 > 0 and price > ma20:
        score += 15
    elif ma20 > 0 and price < ma20:
        score -= 10

    if fair_value > 0 and price < fair_value:
        score += 20
    elif fair_value > 0 and price > fair_value:
        score -= 10

    return score


def generate_daily_strategy() -> dict[str, Any]:
    scan = load_market_scan()

    buy = sorted(scan.get("buy", []), key=_score_item, reverse=True)
    hold = sorted(scan.get("hold", []), key=_score_item, reverse=True)
    sell = sorted(scan.get("sell", []), key=_score_item)
    watch = sorted(scan.get("watch", []), key=_score_item, reverse=True)

    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_buy": buy[:10],
        "today_watch": hold[:10] + watch[:10],
        "risk_list": sell[:10],
        "summary": {
            "top_buy_count": len(buy),
            "watch_count": len(hold) + len(watch),
            "risk_count": len(sell),
        },
    }

    with open(DAILY_STRATEGY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def load_daily_strategy() -> dict[str, Any]:
    if not DAILY_STRATEGY_FILE.exists():
        return {
            "date": None,
            "updated_at": None,
            "top_buy": [],
            "today_watch": [],
            "risk_list": [],
            "summary": {
                "top_buy_count": 0,
                "watch_count": 0,
                "risk_count": 0,
            },
        }

    with open(DAILY_STRATEGY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)