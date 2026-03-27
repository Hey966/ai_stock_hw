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

        data.setdefault("date", "尚未產生")
        data.setdefault("updated_at", "尚未產生")
        data.setdefault("top_buy", [])
        data.setdefault("watch_hold", [])
        data.setdefault("risk_list", [])
        data.setdefault("summary", default_data["summary"])
        return data
    except Exception:
        return default_data


@app.route("/")
@requires_auth
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


@app.route("/stock")
@requires_auth
def stock_page():
    symbol = request.args.get("symbol", "2330").strip()

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


@app.route("/api/market-data")
@requires_auth
def api_market_data():
    try:
        data = load_market_scan_cache()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/daily-selection")
@requires_auth
def api_daily_selection():
    try:
        data = load_daily_selection()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/tools", methods=["GET", "POST"])
@requires_auth
def tools():
    mode = request.values.get("mode", "risk")
    target = request.values.get("target", "").strip()
    benchmark = request.values.get("benchmark", "").strip()
    factors = request.values.get("factors", "").strip()
    positions_text = request.values.get("positions", "").strip()

    price = request.values.get("price", "100").strip()
    face_value = request.values.get("face_value", "100").strip()
    coupon_rate = request.values.get("coupon_rate", "0.03").strip()
    years_to_maturity = request.values.get("years_to_maturity", "5").strip()
    credit_rating = request.values.get("credit_rating", "A").strip()

    risk_result = None
    industry_result = None
    fixed_income_result = None

    stock_labels = []
    stock_weights = []
    industry_labels = []
    industry_weights = []

    try:
        if request.method == "POST":
            if mode == "risk":
                positions = []
                for item in positions_text.split(","):
                    item = item.strip()
                    if not item:
                        continue

                    symbol_part, weight_part = item.split(":")
                    positions.append(
                        {
                            "symbol": symbol_part.strip(),
                            "weight": float(weight_part.strip()),
                        }
                    )

                risk_result = analyze_portfolio_risk(
                    positions=positions,
                    benchmark=benchmark,
                    factors=factors,
                )

                stock_labels = [
                    f"{p['name']} ({p['symbol']})"
                    for p in risk_result.get("positions", [])
                ]
                stock_weights = [
                    p["weight"] for p in risk_result.get("positions", [])
                ]
                industry_labels = [
                    i["industry"]
                    for i in risk_result.get("industry_concentration", [])
                ]
                industry_weights = [
                    i["weight"]
                    for i in risk_result.get("industry_concentration", [])
                ]

            elif mode == "industry":
                industry_result = analyze_industry(
                    target=target,
                    benchmark=benchmark,
                    factors=factors,
                )

            elif mode == "fixed_income":
                fixed_income_result = analyze_fixed_income(
                    target_name=target,
                    benchmark=benchmark,
                    factors=factors,
                    price=float(price),
                    face_value=float(face_value),
                    coupon_rate=float(coupon_rate),
                    years_to_maturity=float(years_to_maturity),
                    credit_rating=credit_rating,
                )

    except Exception as e:
        return render_template_string(
            ERROR_TEMPLATE,
            base_style=BASE_STYLE,
            title="進階分析工具失敗",
            msg=str(e),
        )

    return render_template_string(
        TOOLS_TEMPLATE,
        base_style=BASE_STYLE,
        mode=mode,
        target=target,
        benchmark=benchmark,
        factors=factors,
        positions_text=positions_text,
        price=price,
        face_value=face_value,
        coupon_rate=coupon_rate,
        years_to_maturity=years_to_maturity,
        credit_rating=credit_rating,
        risk_result=risk_result,
        industry_result=industry_result,
        fixed_income_result=fixed_income_result,
        stock_labels=stock_labels,
        stock_weights=stock_weights,
        industry_labels=industry_labels,
        industry_weights=industry_weights,
        live_script=LIVE_SCRIPT,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)