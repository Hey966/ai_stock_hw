import os
import json

from flask import Flask, request, jsonify, render_template_string

from templates_data.live_script import LIVE_SCRIPT
from templates_data.home_template import HOME_TEMPLATE
from templates_data.tools_template import TOOLS_TEMPLATE
from templates_data.error_template import ERROR_TEMPLATE
from templates_data.style import BASE_STYLE
from templates_data.stock_template import STOCK_TEMPLATE
from templates_data.market_template import MARKET_TEMPLATE
from templates_data.daily_template import DAILY_TEMPLATE

from core.auth import requires_auth
from core.market_cache import load_market_scan_cache
from core.ui_helpers import suggestion_class
from core.tw_stock_fundamental import build_structured_report
from core.analysis_tools import (
    analyze_portfolio_risk,
    analyze_industry,
    analyze_fixed_income,
)

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DAILY_SELECTION_PATH = os.path.join(DATA_DIR, "daily_selection.json")


# ========================
# 📦 工具：讀取每日資料
# ========================
def load_daily_selection():
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
# ✅ 健康檢查（Railway 必備）
# ========================
@app.route("/healthz")
def healthz():
    return jsonify({
        "status": "ok",
        "message": "AI stock server running 🚀"
    })


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
    symbol = request.args.get("symbol").strip()

    try:
        report = build_structured_report(symbol)
        valuation = report.get("valuation", {})

        return render_template_string(
            STOCK_TEMPLATE,
            base_style=BASE_STYLE,
            symbol=symbol,
            report=report,
            valuation=valuation,
            suggestion_css=suggestion_class(
                valuation.get("investment_suggestion", "")
            ),
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
# 🔌 API
# ========================
@app.route("/api/market-data")
def api_market_data():
    try:
        data = load_market_scan_cache()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/daily-selection")
def api_daily_selection():
    try:
        data = load_daily_selection()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================
# 🧠 工具頁
# ========================
@app.route("/tools", methods=["GET", "POST"])
@requires_auth
def tools():
    try:
        return render_template_string(
            TOOLS_TEMPLATE,
            base_style=BASE_STYLE,
            live_script=LIVE_SCRIPT,
        )
    except Exception as e:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="工具頁錯誤",
            msg=str(e),
        )


# ========================
# 🚀 啟動（重點）
# ========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False   # 🚨 一定要關掉
    )