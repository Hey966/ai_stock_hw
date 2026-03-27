import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKET_CACHE_FILE = os.path.join(PROJECT_ROOT, "data", "market_scan_cache.json")
DAILY_SELECTION_FILE = os.path.join(PROJECT_ROOT, "data", "daily_selection.json")


def safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default


def load_market_cache():
    if not os.path.exists(MARKET_CACHE_FILE):
        return {}

    try:
        with open(MARKET_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def normalize_items(items, default_signal):
    result = []
    for item in items or []:
        valuation = item.get("valuation", {}) if isinstance(item, dict) else {}
        score = item.get("score", valuation.get("score", 0))

        result.append({
            "symbol": item.get("symbol", ""),
            "company_name": item.get("company_name", ""),
            "suggestion": item.get("suggestion", default_signal),
            "score": safe_int(score, 0),
            "reason": item.get("reason", ""),
            "latest_price": item.get("latest_price", "N/A"),
            "fair_value": item.get("fair_value", "N/A"),
            "ma20": item.get("ma20", "N/A"),
            "updated_at": item.get("updated_at", "")
        })
    return result


def build_daily_selection():
    cache = load_market_cache()

    buy_items = normalize_items(cache.get("buy", []), "買入")
    hold_items = normalize_items(cache.get("hold", []), "持有")
    sell_items = normalize_items(cache.get("sell", []), "賣出")
    suitable_items = normalize_items(cache.get("suitable", []), "適合")

    all_items = buy_items + hold_items + sell_items + suitable_items

    all_items = sorted(
        all_items,
        key=lambda x: (x.get("score", 0), x.get("symbol", "")),
        reverse=True
    )

    top_buy = [x for x in all_items if x["score"] >= 70][:10]
    watch_hold = [x for x in all_items if 55 <= x["score"] < 70][:15]
    risk_list = [x for x in all_items if x["score"] < 55][:15]

    result = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_buy": top_buy,
        "watch_hold": watch_hold,
        "risk_list": risk_list,
        "summary": {
            "top_buy_count": len(top_buy),
            "watch_hold_count": len(watch_hold),
            "risk_list_count": len(risk_list),
            "source_total": len(all_items),
        }
    }

    os.makedirs(os.path.dirname(DAILY_SELECTION_FILE), exist_ok=True)
    with open(DAILY_SELECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result