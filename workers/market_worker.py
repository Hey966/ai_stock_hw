import json
import os
import sys
import time
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.tw_stock_fundamental import build_structured_report
from core.analysis_tools import finmind_get

STATE_FILE = os.path.join(PROJECT_ROOT, "data", "market_worker_state.json")
CACHE_FILE = os.path.join(PROJECT_ROOT, "data", "market_scan_cache.json")
DAILY_SELECTION_FILE = os.path.join(PROJECT_ROOT, "data", "daily_selection.json")

BATCH_SIZE = 5
SLEEP_BETWEEN_SYMBOLS = 5.0
SLEEP_BETWEEN_ROUNDS = 180


def ensure_data_dir():
    os.makedirs(os.path.join(PROJECT_ROOT, "data"), exist_ok=True)


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_int(v, default=0):
    try:
        if v in [None, "", "N/A", "nan", "None"]:
            return default
        return int(float(v))
    except Exception:
        return default


def safe_number(v, default=0):
    if v in [None, "", "N/A", "nan", "None"]:
        return default
    try:
        if isinstance(v, (int, float)):
            return v
        text = str(v).replace(",", "").strip()
        if text == "":
            return default
        if "." in text:
            return float(text)
        return int(text)
    except Exception:
        return default


def get_all_tw_stock_symbols():
    rows = finmind_get("TaiwanStockInfo")
    symbols = []

    for r in rows:
        stock_id = str(r.get("stock_id", "")).strip()
        stock_name = str(r.get("stock_name", "")).strip()
        industry = str(r.get("industry_category", "")).strip()

        if not (stock_id.isdigit() and len(stock_id) == 4):
            continue

        if "ETF" in stock_name.upper():
            continue
        if "ETN" in stock_name.upper():
            continue
        if industry in ["ETF", "ETN", "Index", "大盤"]:
            continue

        symbols.append(stock_id)

    return sorted(list(set(symbols)))


def load_state(total_count):
    ensure_data_dir()

    if not os.path.exists(STATE_FILE):
        return {"cursor": 0, "total": total_count}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "cursor": int(data.get("cursor", 0)),
            "total": total_count,
        }
    except Exception:
        return {"cursor": 0, "total": total_count}


def save_state(cursor, total_count):
    ensure_data_dir()

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "cursor": cursor,
                "total": total_count,
                "updated_at": now_str(),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def empty_cache():
    return {
        "updated_at": "尚未同步",
        "progress": {
            "processed": 0,
            "total": 0,
            "last_symbol": "-",
        },
        "suitable": [],
        "buy": [],
        "hold": [],
        "sell": [],
        "failed": [],
    }


def load_cache():
    ensure_data_dir()

    if not os.path.exists(CACHE_FILE):
        return empty_cache()

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        data.setdefault("updated_at", "尚未同步")
        data.setdefault(
            "progress",
            {
                "processed": 0,
                "total": 0,
                "last_symbol": "-",
            },
        )
        data.setdefault("suitable", [])
        data.setdefault("buy", [])
        data.setdefault("hold", [])
        data.setdefault("sell", [])
        data.setdefault("failed", [])

        return data
    except Exception:
        return empty_cache()


def save_cache(data):
    ensure_data_dir()

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def remove_symbol_from_sections(cache, symbol):
    symbol = str(symbol)

    for section in ["suitable", "buy", "hold", "sell"]:
        cache[section] = [
            x for x in cache.get(section, [])
            if str(x.get("symbol")) != symbol
        ]

    cache["failed"] = [
        x for x in cache.get("failed", [])
        if str(x.get("symbol")) != symbol
    ]


def add_symbol_to_section(cache, section_name, item):
    cache.setdefault(section_name, [])
    cache[section_name].append(item)


def build_failed_item(symbol, reason):
    return {
        "symbol": str(symbol),
        "company_name": str(symbol),
        "suggestion": "適合",
        "score": 0,
        "reason": str(reason),
        "latest_price": 0,
        "fair_value": 0,
        "ma20": 0,
        "updated_at": now_str(),
    }


def analyze_one_symbol(symbol):
    try:
        report = build_structured_report(symbol)
        valuation = report.get("valuation", {}) or {}
        suggestion = str(valuation.get("investment_suggestion", "")).strip()

        item = {
            "symbol": str(report.get("symbol") or symbol),
            "company_name": str(report.get("company_name") or symbol),
            "suggestion": suggestion or "適合",
            "score": safe_int(valuation.get("score", 0), 0),
            "reason": str(valuation.get("reason", "") or ""),
            "latest_price": safe_number(report.get("latest_price", 0), 0),
            "fair_value": safe_number(valuation.get("fair_value", 0), 0),
            "ma20": safe_number(valuation.get("ma20", 0), 0),
            "updated_at": now_str(),
        }

        if suggestion == "買入":
            section = "buy"
        elif suggestion == "持有":
            section = "hold"
        elif suggestion == "賣出":
            section = "sell"
        else:
            section = "suitable"

        return section, item

    except Exception as e:
        return "failed", build_failed_item(symbol, f"fallback: {e}")


def normalize_items(items, default_signal):
    result = []
    for item in items or []:
        result.append(
            {
                "symbol": item.get("symbol", ""),
                "company_name": item.get("company_name", ""),
                "suggestion": item.get("suggestion", default_signal),
                "score": safe_int(item.get("score", 0), 0),
                "reason": item.get("reason", ""),
                "latest_price": safe_number(item.get("latest_price", 0), 0),
                "fair_value": safe_number(item.get("fair_value", 0), 0),
                "ma20": safe_number(item.get("ma20", 0), 0),
                "updated_at": item.get("updated_at", ""),
            }
        )
    return result


def build_daily_selection(cache):
    ensure_data_dir()

    buy_items = normalize_items(cache.get("buy", []), "買入")
    hold_items = normalize_items(cache.get("hold", []), "持有")
    sell_items = normalize_items(cache.get("sell", []), "賣出")
    suitable_items = normalize_items(cache.get("suitable", []), "適合")

    all_items = buy_items + hold_items + sell_items + suitable_items
    all_items = sorted(
        all_items,
        key=lambda x: (x.get("score", 0), x.get("symbol", "")),
        reverse=True,
    )

    top_buy = [x for x in all_items if x["score"] >= 70][:10]
    watch_hold = [x for x in all_items if 55 <= x["score"] < 70][:15]
    risk_list = [x for x in all_items if x["score"] < 55][:15]

    result = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": now_str(),
        "top_buy": top_buy,
        "watch_hold": watch_hold,
        "risk_list": risk_list,
        "summary": {
            "top_buy_count": len(top_buy),
            "watch_hold_count": len(watch_hold),
            "risk_list_count": len(risk_list),
            "source_total": len(all_items),
        },
    }

    with open(DAILY_SELECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def run_one_batch():
    symbols = get_all_tw_stock_symbols()
    total = len(symbols)

    if total == 0:
        print("找不到可分析股票")
        return

    state = load_state(total)
    cache = load_cache()

    start = state["cursor"]
    end = min(start + BATCH_SIZE, total)
    batch_symbols = symbols[start:end]

    if not batch_symbols:
        start = 0
        end = min(BATCH_SIZE, total)
        batch_symbols = symbols[start:end]

    processed = 0
    last_symbol = "-"

    for symbol in batch_symbols:
        last_symbol = symbol

        try:
            section, item = analyze_one_symbol(symbol)
            remove_symbol_from_sections(cache, symbol)

            if section == "failed":
                cache.setdefault("failed", [])
                cache["failed"].append(item)
                print(f"[SKIP] {symbol} 失敗：{item.get('reason', '')}")
            else:
                add_symbol_to_section(cache, section, item)
                print(f"[OK] {symbol} -> {section}")

        except Exception as e:
            remove_symbol_from_sections(cache, symbol)
            cache.setdefault("failed", [])
            cache["failed"].append(build_failed_item(symbol, e))
            print(f"[SKIP] {symbol} 失敗：{e}")

        processed += 1
        time.sleep(SLEEP_BETWEEN_SYMBOLS)

    next_cursor = end if end < total else 0

    cache["updated_at"] = now_str()
    cache["progress"] = {
        "processed": end,
        "total": total,
        "last_symbol": last_symbol,
    }

    save_cache(cache)
    save_state(next_cursor, total)

    try:
        daily_result = build_daily_selection(cache)
        print(
            f"📊 每日選股已更新：Top Buy {daily_result['summary']['top_buy_count']} 檔 / "
            f"觀察 {daily_result['summary']['watch_hold_count']} 檔 / "
            f"風險 {daily_result['summary']['risk_list_count']} 檔"
        )
    except Exception as e:
        print(f"⚠️ 每日選股更新失敗：{e}")

    print(f"✅ 本輪完成，處理 {processed} 檔，下一游標 {next_cursor}/{total}")


def main():
    ensure_data_dir()
    print("🚀 market_worker 啟動")

    while True:
        try:
            run_one_batch()
        except Exception as e:
            print(f"❌ worker 發生錯誤：{e}")

        print(f"⏳ 等待 {SLEEP_BETWEEN_ROUNDS} 秒後進入下一輪")
        time.sleep(SLEEP_BETWEEN_ROUNDS)


if __name__ == "__main__":
    main()