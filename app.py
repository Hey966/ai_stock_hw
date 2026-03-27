from __future__ import annotations

import json
import math
import os
import time
from datetime import datetime
from typing import Any

import pandas as pd
import yfinance as yf
from flask import Flask, jsonify, render_template_string, request

from templates_data.daily_template import DAILY_TEMPLATE
from templates_data.error_template import ERROR_TEMPLATE
from templates_data.home_template import HOME_TEMPLATE
from templates_data.live_script import LIVE_SCRIPT
from templates_data.market_template import MARKET_TEMPLATE
from templates_data.stock_template import STOCK_TEMPLATE
from templates_data.style import BASE_STYLE
from templates_data.tools_template import TOOLS_TEMPLATE

from core.analysis_tools import (
    analyze_fixed_income,
    analyze_industry,
    analyze_portfolio_risk,
)
from core.auth import requires_auth
from core.tw_stock_fundamental import build_structured_report
from core.ui_helpers import suggestion_class

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

MARKET_SCAN_PATH = os.path.join(CACHE_DIR, "market_scan.json")
DAILY_SELECTION_PATH = os.path.join(DATA_DIR, "daily_selection.json")

TWSE_ISIN_URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
TPEX_ISIN_URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"
DEFAULT_SCAN_LIMIT = int(os.environ.get("DEFAULT_SCAN_LIMIT", "50"))
MAX_SCAN_LIMIT = int(os.environ.get("MAX_SCAN_LIMIT", "300"))
REQUEST_SLEEP_SECONDS = float(os.environ.get("SCAN_SLEEP_SECONDS", "0.12"))


# ========================
# 📦 基本工具
# ========================
def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        return float(value)
    except Exception:
        return default


# ========================
# 📦 市場快取讀取
# ========================
def load_market_scan_cache() -> dict[str, Any]:
    default_data = {
        "updated_at": "N/A",
        "total_scanned": 0,
        "buy_count": 0,
        "hold_count": 0,
        "sell_count": 0,
        "watch_count": 0,
        "error_count": 0,
        "buy": [],
        "hold": [],
        "sell": [],
        "watch": [],
        "errors": [],
    }

    if not os.path.exists(MARKET_SCAN_PATH):
        return default_data

    try:
        with open(MARKET_SCAN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return default_data

        for key, value in default_data.items():
            data.setdefault(key, value)

        data["buy_count"] = int(data.get("buy_count", len(data.get("buy", []))))
        data["hold_count"] = int(data.get("hold_count", len(data.get("hold", []))))
        data["sell_count"] = int(data.get("sell_count", len(data.get("sell", []))))
        data["watch_count"] = int(data.get("watch_count", len(data.get("watch", []))))
        data["error_count"] = int(data.get("error_count", len(data.get("errors", []))))
        data["total_scanned"] = int(
            data.get(
                "total_scanned",
                data["buy_count"]
                + data["hold_count"]
                + data["sell_count"]
                + data["watch_count"],
            )
        )
        return data
    except Exception:
        return default_data


# ========================
# 📦 每日策略讀取
# ========================
def load_daily_selection() -> dict[str, Any]:
    default_data = {
        "date": "尚未產生",
        "updated_at": "尚未產生",
        "top_buy": [],
        "watch_hold": [],
        "risk_list": [],
        "summary": {
            "top_buy_count": 0,
            "watch_hold_count": 0,
            "risk_list_count": 0,
            "source_total": 0,
        },
    }

    if not os.path.exists(DAILY_SELECTION_PATH):
        return default_data

    try:
        with open(DAILY_SELECTION_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return default_data

        data.setdefault("date", "尚未產生")
        data.setdefault("updated_at", "尚未產生")
        data.setdefault("top_buy", [])
        data.setdefault("watch_hold", [])
        data.setdefault("risk_list", [])
        data.setdefault("summary", default_data["summary"])

        if not isinstance(data["summary"], dict):
            data["summary"] = default_data["summary"]

        data["summary"].setdefault("top_buy_count", len(data["top_buy"]))
        data["summary"].setdefault("watch_hold_count", len(data["watch_hold"]))
        data["summary"].setdefault("risk_list_count", len(data["risk_list"]))
        data["summary"].setdefault(
            "source_total",
            len(data["top_buy"]) + len(data["watch_hold"]) + len(data["risk_list"]),
        )

        return data
    except Exception:
        return default_data


# ========================
# 📦 台股清單
# ========================
def _parse_isin_table(url: str, suffix: str) -> list[dict[str, str]]:
    tables = pd.read_html(url, encoding="utf-8")
    if not tables:
        return []

    df = tables[0].copy()
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "raw_name"})

    results: list[dict[str, str]] = []
    for _, row in df.iterrows():
        raw = str(row.get("raw_name", "")).strip()
        if not raw:
            continue

        parts = raw.split()
        if len(parts) < 2:
            continue

        code = parts[0].strip()
        name = " ".join(parts[1:]).strip()

        if not code.isdigit() or len(code) != 4:
            continue

        results.append(
            {
                "symbol": code,
                "name": name,
                "ticker": f"{code}{suffix}",
            }
        )
    return results


def get_tw_stock_universe() -> list[dict[str, str]]:
    universe = []
    universe.extend(_parse_isin_table(TWSE_ISIN_URL, ".TW"))
    universe.extend(_parse_isin_table(TPEX_ISIN_URL, ".TWO"))

    seen = set()
    deduped = []
    for item in universe:
        ticker = item["ticker"]
        if ticker in seen:
            continue
        seen.add(ticker)
        deduped.append(item)
    return deduped


# ========================
# 📦 掃描與策略
# ========================
def estimate_fair_value(info: dict[str, Any], price: float) -> float:
    target_mean = safe_float(info.get("targetMeanPrice"))
    target_median = safe_float(info.get("targetMedianPrice"))
    fifty_two_week_high = safe_float(info.get("fiftyTwoWeekHigh"))
    fifty_two_week_low = safe_float(info.get("fiftyTwoWeekLow"))

    if target_mean > 0:
        return round(target_mean, 2)
    if target_median > 0:
        return round(target_median, 2)
    if fifty_two_week_high > 0 and fifty_two_week_low > 0:
        return round((fifty_two_week_high + fifty_two_week_low) / 2, 2)
    return round(price, 2)


def normalize_signal(price: float, ma20: float, ma60: float, fair_value: float) -> tuple[str, str]:
    above_ma20 = ma20 > 0 and price >= ma20
    above_ma60 = ma60 > 0 and price >= ma60
    below_fair = fair_value > 0 and price <= fair_value * 0.95
    above_fair = fair_value > 0 and price >= fair_value * 1.08

    if above_ma20 and above_ma60 and below_fair:
        return "BUY", "價格站上均線且低於估計合理價"
    if above_ma20 and not above_fair:
        return "HOLD", "價格位於短期均線之上"
    if not above_ma20 and above_fair:
        return "SELL", "價格跌破短均線且高於估計合理價"
    return "WATCH", "等待更明確趨勢訊號"


def analyze_stock_for_scan(stock: dict[str, str]) -> dict[str, Any] | None:
    ticker = stock["ticker"]
    symbol = stock["symbol"]
    company_name = stock["name"]

    try:
        yf_ticker = yf.Ticker(ticker)
        hist = yf_ticker.history(period="6mo", auto_adjust=False)
        if hist is None or hist.empty:
            return None

        closes = hist["Close"].dropna()
        if closes.empty:
            return None

        price = round(float(closes.iloc[-1]), 2)
        ma20 = round(float(closes.tail(20).mean()), 2) if len(closes) >= 20 else 0.0
        ma60 = round(float(closes.tail(60).mean()), 2) if len(closes) >= 60 else 0.0

        info: dict[str, Any] = {}
        try:
            info = yf_ticker.fast_info or {}
        except Exception:
            info = {}

        fair_value = estimate_fair_value(info, price)
        signal, reason = normalize_signal(price, ma20, ma60, fair_value)

        change_pct = 0.0
        if len(closes) >= 2 and safe_float(closes.iloc[-2]) > 0:
            change_pct = round((price - float(closes.iloc[-2])) / float(closes.iloc[-2]) * 100, 2)

        return {
            "symbol": symbol,
            "ticker": ticker,
            "company_name": company_name,
            "price": price,
            "ma20": ma20,
            "ma60": ma60,
            "fair_value": fair_value,
            "daily_change_pct": change_pct,
            "signal": signal,
            "reason": reason,
            "valuation_reason": "targetMeanPrice / 52週區間推估",
        }
    except Exception as exc:
        return {
            "symbol": symbol,
            "ticker": ticker,
            "company_name": company_name,
            "signal": "ERROR",
            "error": str(exc),
        }


def _score_scan_item(item: dict[str, Any]) -> float:
    score = 0.0
    signal = str(item.get("signal", "")).upper()
    price = safe_float(item.get("price"))
    ma20 = safe_float(item.get("ma20"))
    ma60 = safe_float(item.get("ma60"))
    fair_value = safe_float(item.get("fair_value"))
    change_pct = safe_float(item.get("daily_change_pct"))

    if signal == "BUY":
        score += 50
    elif signal == "HOLD":
        score += 20
    elif signal == "SELL":
        score -= 30

    if ma20 > 0 and price > ma20:
        score += 12
    if ma60 > 0 and price > ma60:
        score += 8
    if fair_value > 0 and price < fair_value:
        score += 15
    if fair_value > 0 and price > fair_value:
        score -= 10

    score += max(min(change_pct, 8), -8)
    return round(score, 2)


def run_market_scan(limit: int | None = None) -> dict[str, Any]:
    universe = get_tw_stock_universe()

    if limit is None:
        limit = DEFAULT_SCAN_LIMIT

    limit = max(1, min(limit, MAX_SCAN_LIMIT))
    universe = universe[:limit]

    results = []
    for stock in universe:
        item = analyze_stock_for_scan(stock)
        if item:
            results.append(item)
        time.sleep(REQUEST_SLEEP_SECONDS)

    valid = [r for r in results if r.get("signal") != "ERROR"]
    errors = [r for r in results if r.get("signal") == "ERROR"]

    buy = sorted([r for r in valid if r.get("signal") == "BUY"], key=_score_scan_item, reverse=True)
    hold = sorted([r for r in valid if r.get("signal") == "HOLD"], key=_score_scan_item, reverse=True)
    sell = sorted([r for r in valid if r.get("signal") == "SELL"], key=_score_scan_item)
    watch = sorted([r for r in valid if r.get("signal") == "WATCH"], key=_score_scan_item, reverse=True)

    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_scanned": len(valid),
        "buy_count": len(buy),
        "hold_count": len(hold),
        "sell_count": len(sell),
        "watch_count": len(watch),
        "error_count": len(errors),
        "buy": buy,
        "hold": hold,
        "sell": sell,
        "watch": watch,
        "errors": errors[:30],
    }

    with open(MARKET_SCAN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def generate_daily_selection() -> dict[str, Any]:
    scan = load_market_scan_cache()

    buy = sorted(scan.get("buy", []), key=_score_scan_item, reverse=True)
    hold = sorted(scan.get("hold", []), key=_score_scan_item, reverse=True)
    watch = sorted(scan.get("watch", []), key=_score_scan_item, reverse=True)
    sell = sorted(scan.get("sell", []), key=_score_scan_item)

    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_buy": buy[:10],
        "watch_hold": (hold[:5] + watch[:5])[:10],
        "risk_list": sell[:10],
        "summary": {
            "top_buy_count": len(buy),
            "watch_hold_count": len(hold) + len(watch),
            "risk_list_count": len(sell),
            "source_total": scan.get("total_scanned", 0),
        },
    }

    with open(DAILY_SELECTION_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


# ========================
# ✅ 健康檢查（Railway 必備）
# ========================
@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "message": "AI stock server running 🚀"})


# ========================
# 🏠 首頁
# ========================
@app.route("/")
def home():
    try:
        market_sections = load_market_scan_cache()
        daily_selection = load_daily_selection()

        return render_template_string(
            HOME_TEMPLATE,
            base_style=BASE_STYLE,
            market_sections=market_sections,
            daily_selection=daily_selection,
            live_script=LIVE_SCRIPT,
        )
    except Exception as e:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="首頁載入失敗",
            msg=str(e),
        )


# ========================
# 📊 個股分析
# ========================
@app.route("/stock")
@requires_auth
def stock_page():
    symbol = (request.args.get("symbol") or "").strip()
    if not symbol:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="個股分析失敗",
            msg="缺少 symbol 參數",
        )

    try:
        report = build_structured_report(symbol)
        valuation = report.get("valuation", {})

        return render_template_string(
            STOCK_TEMPLATE,
            base_style=BASE_STYLE,
            symbol=symbol,
            report=report,
            valuation=valuation,
            suggestion_css=suggestion_class(valuation.get("investment_suggestion", "")),
            live_script=LIVE_SCRIPT,
        )
    except Exception as e:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="個股分析失敗",
            msg=str(e),
        )


# ========================
# 📈 市場頁
# ========================
@app.route("/market")
@requires_auth
def market_page():
    try:
        market_sections = load_market_scan_cache()

        return render_template_string(
            MARKET_TEMPLATE,
            base_style=BASE_STYLE,
            market_sections=market_sections,
            live_script=LIVE_SCRIPT,
        )
    except Exception as e:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="市場掃描頁載入失敗",
            msg=str(e),
        )


# ========================
# 📅 每日策略
# ========================
@app.route("/daily")
@requires_auth
def daily_page():
    try:
        daily_selection = load_daily_selection()

        return render_template_string(
            DAILY_TEMPLATE,
            base_style=BASE_STYLE,
            daily_selection=daily_selection,
            live_script=LIVE_SCRIPT,
        )
    except Exception as e:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="今日策略頁載入失敗",
            msg=str(e),
        )


# ========================
# 🔌 原有 API
# ========================
@app.route("/api/market-data")
def api_market_data():
    try:
        return jsonify(load_market_scan_cache())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/daily-selection")
def api_daily_selection():
    try:
        return jsonify(load_daily_selection())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================
# 🔌 新增掃描 API
# ========================
@app.route("/api/market-scan")
def api_market_scan():
    try:
        return jsonify(load_market_scan_cache())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/market-scan/run", methods=["POST"])
def api_market_scan_run():
    try:
        limit = request.args.get("limit", type=int)
        data = run_market_scan(limit=limit)
        return jsonify({"status": "ok", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/api/daily-strategy")
def api_daily_strategy():
    try:
        return jsonify(load_daily_selection())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/daily-strategy/run", methods=["POST"])
def api_daily_strategy_run():
    try:
        if request.args.get("scan_first", "1") == "1":
            limit = request.args.get("limit", type=int)
            run_market_scan(limit=limit)
        data = generate_daily_selection()
        return jsonify({"status": "ok", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/api/tw-universe")
def api_tw_universe():
    try:
        universe = get_tw_stock_universe()
        return jsonify({"count": len(universe), "items": universe[:200]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================
# 🧠 工具頁
# ========================
@app.route("/tools", methods=["GET", "POST"])
@requires_auth
def tools():
    try:
        result: dict[str, Any] | None = None
        error_msg = None

        if request.method == "POST":
            tool_type = (request.form.get("tool_type") or "").strip()
            payload = (request.form.get("payload") or "").strip()

            try:
                parsed_payload = json.loads(payload) if payload else {}
                if tool_type == "portfolio_risk":
                    result = analyze_portfolio_risk(parsed_payload)
                elif tool_type == "industry":
                    result = analyze_industry(parsed_payload)
                elif tool_type == "fixed_income":
                    result = analyze_fixed_income(parsed_payload)
                else:
                    error_msg = "不支援的工具模式"
            except Exception as exc:
                error_msg = str(exc)

        return render_template_string(
            TOOLS_TEMPLATE,
            base_style=BASE_STYLE,
            live_script=LIVE_SCRIPT,
            result=result,
            error_msg=error_msg,
        )
    except Exception as e:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="工具頁錯誤",
            msg=str(e),
        )


# ========================
# 🚀 啟動
# ========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
