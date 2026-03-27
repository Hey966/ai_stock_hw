from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from services.tw_universe import get_tw_stock_universe

# 改成你的實際分析函式路徑
from app.analysis import analyze_stock

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

MARKET_SCAN_FILE = CACHE_DIR / "market_scan.json"


def normalize_signal(signal: str) -> str:
    s = str(signal).strip().upper()
    if s in {"BUY", "STRONG_BUY"}:
        return "BUY"
    if s in {"SELL", "STRONG_SELL"}:
        return "SELL"
    if s in {"HOLD", "NEUTRAL"}:
        return "HOLD"
    return "WATCH"


def safe_analyze_stock(stock: dict[str, str]) -> dict[str, Any] | None:
    try:
        result = analyze_stock(stock["ticker"])
        if not result:
            return None

        result["symbol"] = result.get("symbol") or stock["symbol"]
        result["ticker"] = result.get("ticker") or stock["ticker"]
        result["company_name"] = result.get("company_name") or stock["name"]
        result["signal"] = normalize_signal(result.get("signal", "WATCH"))

        return result
    except Exception as e:
        return {
            "symbol": stock["symbol"],
            "ticker": stock["ticker"],
            "company_name": stock["name"],
            "signal": "ERROR",
            "error": str(e),
        }


def classify_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [r for r in results if r.get("signal") != "ERROR"]

    buy = [r for r in valid if r.get("signal") == "BUY"]
    hold = [r for r in valid if r.get("signal") == "HOLD"]
    sell = [r for r in valid if r.get("signal") == "SELL"]
    watch = [r for r in valid if r.get("signal") == "WATCH"]
    errors = [r for r in results if r.get("signal") == "ERROR"]

    return {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_scanned": len(valid),
        "error_count": len(errors),
        "buy_count": len(buy),
        "hold_count": len(hold),
        "sell_count": len(sell),
        "watch_count": len(watch),
        "buy": buy,
        "hold": hold,
        "sell": sell,
        "watch": watch,
        "errors": errors,
    }


def save_market_scan(data: dict[str, Any]) -> None:
    with open(MARKET_SCAN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_market_scan() -> dict[str, Any]:
    if not MARKET_SCAN_FILE.exists():
        return {
            "updated_at": None,
            "total_scanned": 0,
            "error_count": 0,
            "buy_count": 0,
            "hold_count": 0,
            "sell_count": 0,
            "watch_count": 0,
            "buy": [],
            "hold": [],
            "sell": [],
            "watch": [],
            "errors": [],
        }

    with open(MARKET_SCAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def run_market_scan(limit: int | None = None) -> dict[str, Any]:
    universe = get_tw_stock_universe()

    if limit is not None:
        universe = universe[:limit]

    results = []
    for stock in universe:
        item = safe_analyze_stock(stock)
        if item:
            results.append(item)

    summary = classify_results(results)
    save_market_scan(summary)
    return summary