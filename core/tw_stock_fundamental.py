import os
import json
import time
from datetime import datetime
import requests
import yfinance as yf
from collections import defaultdict

from core.price_analysis import analyze_price_structure

from .finmind_auth import get_finmind_token
from .scoring_engine import build_score_report
from .news_analysis import analyze_stock_news

BASE_URL = "https://api.finmindtrade.com/api/v4/data"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")
CACHE_TTL_SECONDS = 60 * 30  # 30 分鐘


def ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def cache_path(key: str) -> str:
    safe_key = key.replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
    return os.path.join(CACHE_DIR, f"{safe_key}.json")


def load_cache(key: str, force_refresh: bool = False):
    if force_refresh:
        return None

    path = cache_path(key)
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if time.time() - payload["ts"] < CACHE_TTL_SECONDS:
            return payload["data"]
    except Exception:
        return None
    return None


def save_cache(key: str, data):
    ensure_cache_dir()
    path = cache_path(key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"ts": time.time(), "data": data}, f, ensure_ascii=False)


def get_headers():
    token = get_finmind_token()
    return {"Authorization": f"Bearer {token}"}


def finmind_get(dataset: str, force_refresh: bool = False, **params):
    query = {"dataset": dataset}
    query.update(params)

    cache_key = dataset + "_" + "_".join(f"{k}={v}" for k, v in sorted(query.items()))
    cached = load_cache(cache_key, force_refresh=force_refresh)
    if cached is not None:
        return cached

    resp = requests.get(BASE_URL, headers=get_headers(), params=query, timeout=20)
    if resp.status_code != 200:
        raise Exception(f"FinMind API 錯誤，狀態碼: {resp.status_code}")

    data = resp.json()
    if "data" not in data:
        raise Exception(f"FinMind 回傳格式異常: {data}")

    save_cache(cache_key, data["data"])
    return data["data"]


def safe_float(v, default=None):
    try:
        if v is None or v == "":
            return default
        if isinstance(v, str):
            v = v.replace(",", "").strip()
            if v == "":
                return default
        return float(v)
    except Exception:
        return default


def safe_int(v, default=0):
    try:
        if v is None or v == "":
            return default
        return int(float(v))
    except Exception:
        return default


def format_pct(v):
    if v is None:
        return "0.00%"
    return f"{v * 100:.2f}%"


def format_ratio(v):
    if v is None:
        return "0"
    return f"{v:.2f}"


def format_money(v):
    if v is None:
        return "0"
    v = float(v)
    if abs(v) >= 1_000_000_000:
        return f"{v / 1_000_000_000:.2f} B"
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.2f} M"
    return f"{v:,.0f}"


def _normalize_datetime(value):
    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        return value

    try:
        if hasattr(value, "to_pydatetime"):
            return value.to_pydatetime()
    except Exception:
        pass

    if isinstance(value, (int, float)):
        try:
            ts = float(value)
            if ts > 1_000_000_000_000:
                ts = ts / 1000.0
            return datetime.fromtimestamp(ts)
        except Exception:
            return None

    text = str(value).strip()
    if not text:
        return None

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text[:19], fmt)
        except Exception:
            continue
    return None


def _format_quote_datetime(value):
    dt = _normalize_datetime(value)
    if dt is None:
        return None
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
        return dt.strftime("%Y-%m-%d")
    return dt.strftime("%Y-%m-%d %H:%M")


def get_live_quote(symbol: str):
    for suffix in (".TW", ".TWO"):
        ticker = f"{symbol}{suffix}"
        try:
            yf_ticker = yf.Ticker(ticker)

            price = None
            quote_dt = None
            source = None

            try:
                fast_info = yf_ticker.fast_info or {}
            except Exception:
                fast_info = {}

            if isinstance(fast_info, dict):
                raw_price = (
                    fast_info.get("lastPrice")
                    or fast_info.get("last_price")
                    or fast_info.get("regularMarketPrice")
                    or fast_info.get("currentPrice")
                )
                price = safe_float(raw_price, None)
                quote_dt = _normalize_datetime(
                    fast_info.get("lastPriceTime") or fast_info.get("regularMarketTime")
                )
                if price not in (None, 0):
                    source = "yfinance_fast_info"

            if price in (None, 0):
                hist = yf_ticker.history(period="5d", interval="1d", auto_adjust=False)
                if hist is not None and not hist.empty:
                    closes = hist["Close"].dropna()
                    if not closes.empty:
                        price = safe_float(closes.iloc[-1], None)
                        quote_dt = _normalize_datetime(closes.index[-1])
                        source = source or "yfinance_history"

            if price not in (None, 0):
                return {
                    "ticker": ticker,
                    "price": round(float(price), 2),
                    "date": _format_quote_datetime(quote_dt),
                    "source": source or "yfinance",
                }
        except Exception:
            continue

    return {
        "ticker": None,
        "price": None,
        "date": None,
        "source": "finmind",
    }


def get_stock_info(symbol: str, force_refresh: bool = False):
    rows = finmind_get("TaiwanStockInfo", force_refresh=force_refresh)
    for row in rows:
        if str(row.get("stock_id", "")).strip() == symbol:
            return row
    raise Exception("找不到該股票代號，請確認是否為台股代號。")


def get_price_data(symbol: str, force_refresh: bool = False):
    return finmind_get("TaiwanStockPrice", force_refresh=force_refresh, data_id=symbol, start_date="2024-01-01")


def get_per_data(symbol: str, force_refresh: bool = False):
    return finmind_get("TaiwanStockPER", force_refresh=force_refresh, data_id=symbol, start_date="2024-01-01")


def get_financial_statements(symbol: str, force_refresh: bool = False):
    return finmind_get("TaiwanStockFinancialStatements", force_refresh=force_refresh, data_id=symbol, start_date="2021-01-01")


def get_balance_sheet(symbol: str, force_refresh: bool = False):
    return finmind_get("TaiwanStockBalanceSheet", force_refresh=force_refresh, data_id=symbol, start_date="2021-01-01")


def get_month_revenue(symbol: str, force_refresh: bool = False):
    return finmind_get("TaiwanStockMonthRevenue", force_refresh=force_refresh, data_id=symbol, start_date="2021-01-01")


def latest_row(rows, key="date"):
    if not rows:
        return None
    return sorted(rows, key=lambda x: x.get(key, ""))[-1]


def build_statement_map(rows):
    result = defaultdict(dict)
    for row in rows:
        date = row.get("date")
        typ = row.get("type")
        value = safe_float(row.get("value"))
        origin_name = row.get("origin_name", "")
        if date and typ:
            result[date][typ] = value
            result[date][origin_name] = value
    return result


def pick_value(d: dict, candidates):
    for key in candidates:
        if key in d and d[key] is not None:
            return d[key]
    return None


def calc_annual_revenue_from_monthly(rows):
    annual = defaultdict(float)
    for row in rows:
        year = str(row.get("revenue_year", "")) or str(row.get("date", ""))[:4]
        revenue = safe_float(row.get("revenue"), 0)
        if year:
            annual[year] += revenue

    items = sorted(annual.items(), key=lambda x: x[0], reverse=True)[:3]
    items.reverse()

    result = []
    for y, v in items:
        result.append({
            "year": y,
            "revenue": int(v),
            "revenue_raw": float(v)
        })
    return result


def calc_latest_price_metrics(price_rows, per_rows):
    if not price_rows:
        return {"close": 0, "spread": 0, "price_date": None, "per": None, "pbr": None}

    latest_price = latest_row(price_rows, "date")
    latest_per = latest_row(per_rows, "date") if per_rows else None

    close = safe_float(latest_price.get("close"), 0)
    spread = safe_float(latest_price.get("spread"), 0)

    if latest_per:
        per = safe_float(latest_per.get("PER"))
        pbr = safe_float(latest_per.get("PBR"))
    else:
        per = None
        pbr = None

    return {
        "close": close,
        "spread": spread,
        "price_date": latest_price.get("date"),
        "per": per,
        "pbr": pbr,
    }


def calculate_ma20(price_rows):
    closes = []
    for row in price_rows:
        close_v = safe_float(row.get("close"))
        if close_v is not None:
            closes.append(close_v)

    if len(closes) < 20:
        return 0

    return round(sum(closes[-20:]) / 20, 2)


def calc_gross_margin(fin_stmt_map):
    if not fin_stmt_map:
        return None

    latest_date = sorted(fin_stmt_map.keys())[-1]
    row = fin_stmt_map[latest_date]

    gross_profit = pick_value(row, [
        "GrossProfit",
        "營業毛利（毛損）淨額",
        "營業毛利（毛損）"
    ])
    revenue = pick_value(row, [
        "Revenue",
        "TotalRevenue",
        "營業收入合計",
        "收入合計",
        "營業收入淨額"
    ])

    if gross_profit is None or revenue in (None, 0):
        return None
    return gross_profit / revenue


def calc_ttm_net_income(fin_stmt_map):
    dates = sorted(fin_stmt_map.keys(), reverse=True)[:4]
    if not dates:
        return None

    total = 0
    found = False
    for d in dates:
        row = fin_stmt_map[d]
        income = pick_value(row, [
            "IncomeAfterTaxes",
            "ProfitLoss",
            "本期淨利（淨損）",
            "本期稅後淨利（淨損）",
        ])
        if income is not None:
            total += income
            found = True

    return total if found else None


def calc_roe(fin_stmt_map, balance_map):
    ttm_income = calc_ttm_net_income(fin_stmt_map)
    if ttm_income is None or not balance_map:
        return None

    latest_date = sorted(balance_map.keys())[-1]
    row = balance_map[latest_date]

    equity = pick_value(row, [
        "Equity",
        "TotalEquity",
        "權益總額",
        "權益總計",
        "歸屬於母公司業主之權益合計",
    ])

    if equity in (None, 0):
        return None
    return ttm_income / equity


def calc_debt_ratio(balance_map):
    if not balance_map:
        return None

    latest_date = sorted(balance_map.keys())[-1]
    row = balance_map[latest_date]

    assets = pick_value(row, [
        "TotalAssets",
        "資產總額",
        "資產總計",
    ])
    liabilities = pick_value(row, [
        "TotalLiabilities",
        "負債總額",
        "負債總計",
        "負債合計",
    ])

    if assets in (None, 0) or liabilities is None:
        return None
    return liabilities / assets


def calc_debt_to_equity(balance_map):
    if not balance_map:
        return None

    latest_date = sorted(balance_map.keys())[-1]
    row = balance_map[latest_date]

    liabilities = pick_value(row, [
        "TotalLiabilities",
        "負債總額",
        "負債總計",
        "負債合計",
    ])
    equity = pick_value(row, [
        "Equity",
        "TotalEquity",
        "權益總額",
        "權益總計",
        "歸屬於母公司業主之權益合計",
    ])

    if liabilities is None or equity in (None, 0):
        return None
    return liabilities / equity


def overview_from_info(info):
    stock_name = info.get("stock_name", "未知公司")
    industry = info.get("industry_category", "N/A")
    market = info.get("type", "N/A")

    return {
        "company_name": stock_name,
        "industry_category": industry,
        "main_products_services": f"{stock_name} 屬於 {industry} 類股，詳細產品結構建議再補公司年報或公開說明書。",
        "market_position": f"目前市場別：{market}。市場地位可再搭配市值、毛利率與ROE綜合觀察。"
    }


def moat_analysis(info, gross_margin, roe):
    industry = str(info.get("industry_category", ""))

    points = []
    if "半導體" in industry:
        points.append("半導體產業通常具技術門檻、資本支出門檻與客戶認證門檻。")
    elif "電子" in industry:
        points.append("電子業差異化多來自規模經濟、良率控制、供應鏈整合與客戶關係。")
    elif "航運" in industry:
        points.append("航運業優勢通常來自船隊規模、航線配置與成本控管能力。")
    else:
        points.append("競爭優勢需觀察品牌、通路、成本優勢與客戶黏著度。")

    if gross_margin is not None:
        if gross_margin >= 0.40:
            points.append("毛利率偏高，顯示具有一定議價能力。")
        elif gross_margin >= 0.20:
            points.append("毛利率中等，競爭力尚可但仍需追蹤。")
        else:
            points.append("毛利率偏低，代表較依賴規模或成本效率。")

    if roe is not None:
        if roe >= 0.15:
            points.append("ROE 良好，資本效率不錯。")
        elif roe >= 0.08:
            points.append("ROE 中等，仍可接受。")
        else:
            points.append("ROE 偏弱，獲利效率需留意。")

    return " ".join(points)


def risk_analysis(info, debt_ratio, roe, per):
    industry = str(info.get("industry_category", ""))

    points = []

    if debt_ratio is not None:
        if debt_ratio > 0.6:
            points.append("負債比偏高，景氣轉弱時財務壓力較大。")
        elif debt_ratio > 0.4:
            points.append("負債比中等，需持續追蹤現金流。")
        else:
            points.append("負債比相對可控。")

    if roe is not None and roe < 0.08:
        points.append("ROE 偏弱，代表資本報酬效率不足。")

    if per is not None and per > 25:
        points.append("本益比偏高，市場已反映較高成長預期。")

    if "半導體" in industry:
        points.append("需留意景氣循環、庫存調整與地緣政治風險。")
    elif "航運" in industry:
        points.append("需留意運價波動、供需循環與油價變動。")
    else:
        points.append("需留意產業競爭、需求波動與原物料風險。")

    return " ".join(points)


def estimate_fair_value(latest_price, trailing_pe, industry_category):
    price = safe_float(latest_price)
    pe = safe_float(trailing_pe)

    if price in (None, 0) or pe in (None, 0):
        return 0, "N/A"

    eps = price / pe

    target_pe = 15
    pe_range = "12 - 18"

    if "半導體" in industry_category:
        target_pe = 22
        pe_range = "18 - 28"
    elif "電子" in industry_category:
        target_pe = 18
        pe_range = "15 - 22"
    elif "航運" in industry_category:
        target_pe = 10
        pe_range = "8 - 12"

    fair_value = round(eps * target_pe, 2)
    return fair_value, pe_range


def valuation_judgment(per):
    if per is None:
        return {
            "pe_range": "N/A",
            "investment_suggestion": "持有",
            "reason": "暫缺本益比資料，建議先觀察。"
        }

    if per < 12:
        return {
            "pe_range": "< 12",
            "investment_suggestion": "買入",
            "reason": "本益比偏低，若基本面穩定，具相對估值吸引力。"
        }
    if per < 20:
        return {
            "pe_range": "12 - 20",
            "investment_suggestion": "持有",
            "reason": "本益比位於合理區間，適合持續追蹤。"
        }
    return {
        "pe_range": "> 20",
        "investment_suggestion": "賣出",
        "reason": "本益比偏高，需留意估值修正風險。"
    }


def build_latest_price_judgment(latest_price, latest_price_date, ma20, fair_value, base_suggestion, base_reason):
    price = safe_float(latest_price)
    ma20 = safe_float(ma20)
    fair_value = safe_float(fair_value)

    suggestion = base_suggestion or "持有"
    signal_reason = "沿用原本評估結論。"

    if price not in (None, 0):
        if fair_value > 0 and price <= fair_value * 0.95 and (ma20 == 0 or price >= ma20 * 0.97):
            suggestion = "買入"
            signal_reason = f"最新股價 {price:.2f} 低於合理價 {fair_value:.2f}，且價格未明顯弱於 MA20。"
        elif fair_value > 0 and price >= fair_value * 1.08 and ma20 > 0 and price < ma20:
            suggestion = "賣出"
            signal_reason = f"最新股價 {price:.2f} 高於合理價 {fair_value:.2f}，且已跌破 MA20 {ma20:.2f}。"
        elif ma20 > 0 and price >= ma20:
            suggestion = "持有"
            signal_reason = f"最新股價 {price:.2f} 位於 MA20 {ma20:.2f} 之上，短線趨勢仍偏穩。"
        elif ma20 > 0 and price < ma20 and fair_value > 0 and price > fair_value * 1.02:
            suggestion = "賣出"
            signal_reason = f"最新股價 {price:.2f} 跌破 MA20 {ma20:.2f}，且價格未明顯便宜。"
        elif fair_value > 0 and price < fair_value:
            suggestion = "持有"
            signal_reason = f"最新股價 {price:.2f} 低於合理價 {fair_value:.2f}，但仍需觀察趨勢確認。"
        else:
            suggestion = base_suggestion or "持有"
            signal_reason = f"最新股價 {price:.2f} 與合理價、均線關係接近中性。"

    date_text = f"價格日期：{latest_price_date}。" if latest_price_date else ""
    reason_parts = [date_text, f"最新股價判斷：{signal_reason}"]
    if base_reason:
        reason_parts.append(f"基本面 / 估值補充：{base_reason}")
    full_reason = " ".join(part.strip() for part in reason_parts if part and part.strip())

    return {
        "suggestion": suggestion,
        "signal_reason": signal_reason,
        "reason": full_reason,
    }


def build_structured_report(symbol: str, force_refresh: bool = False):
    symbol = symbol.strip()

    try:
        info = get_stock_info(symbol, force_refresh=force_refresh)
    except Exception:
        info = {
            "stock_name": symbol,
            "industry_category": "N/A",
            "type": "N/A"
        }

    try:
        price_rows = get_price_data(symbol, force_refresh=force_refresh)
    except Exception:
        price_rows = []

    try:
        per_rows = get_per_data(symbol, force_refresh=force_refresh)
    except Exception:
        per_rows = []

    try:
        fin_rows = get_financial_statements(symbol, force_refresh=force_refresh)
    except Exception:
        fin_rows = []

    try:
        balance_rows = get_balance_sheet(symbol, force_refresh=force_refresh)
    except Exception:
        balance_rows = []

    try:
        revenue_rows = get_month_revenue(symbol, force_refresh=force_refresh)
    except Exception:
        revenue_rows = []

    fin_map = build_statement_map(fin_rows)
    balance_map = build_statement_map(balance_rows)

    overview = overview_from_info(info)
    rev3y = calc_annual_revenue_from_monthly(revenue_rows)
    latest_price = calc_latest_price_metrics(price_rows, per_rows)
    live_quote = get_live_quote(symbol)

    try:
        news_analysis = analyze_stock_news(
            symbol=symbol,
            company_name=overview["company_name"],
            industry=overview["industry_category"],
            force_refresh=force_refresh,
        )
    except Exception:
        news_analysis = {
            "symbol": symbol,
            "company_name": overview["company_name"],
            "headline_count": 0,
            "positive_count": 0,
            "negative_count": 0,
            "sentiment_score": 0,
            "news_score": 10,
            "risk_level": "中",
            "summary": "新聞資料暫時無法取得，先以中性分數處理。",
            "top_news": [],
        }

    gross_margin = calc_gross_margin(fin_map)
    roe = calc_roe(fin_map, balance_map)
    debt_ratio = calc_debt_ratio(balance_map)
    debt_to_equity = calc_debt_to_equity(balance_map)
    ma20 = calculate_ma20(price_rows)
    price_analysis = analyze_price_structure(price_rows)

    moat = moat_analysis(info, gross_margin, roe)
    risk = risk_analysis(info, debt_ratio, roe, latest_price["per"])

    reference_price = live_quote.get("price") or latest_price["close"]
    fair_value, fair_pe_range = estimate_fair_value(
        latest_price=reference_price,
        trailing_pe=latest_price["per"],
        industry_category=overview["industry_category"],
    )

    try:
        score_report = build_score_report(
            latest_price=reference_price,
            fair_value=fair_value,
            trailing_pe=latest_price["per"],
            industry_category=overview["industry_category"],
            roe=(roe * 100 if roe is not None else None),
            gross_margin=(gross_margin * 100 if gross_margin is not None else None),
            debt_ratio=(debt_ratio * 100 if debt_ratio is not None else None),
            revenue_trend_3y=rev3y,
            ma20=ma20,
        )
    except Exception:
        score_report = {
            "total_score": 0,
            "valuation_score": 0,
            "quality_score": 0,
            "growth_score": 0,
            "technical_score": 0,
            "investment_suggestion": "適合",
            "reason": "評分資料不足，先以保守模式顯示。"
        }

    news_score = safe_int(news_analysis.get("news_score", 10), 10)

    technical_score = min(
        100,
        safe_int(score_report.get("technical_score", 0), 0)
        + safe_int(price_analysis.get("score", 0), 0)
    )
    score_report["technical_score"] = technical_score

    base_total_score = safe_int(score_report.get("total_score", 0), 0)
    blended_total_score = min(100, round(base_total_score * 0.8 + news_score * 1.0))

    old_valuation = valuation_judgment(latest_price["per"])

    displayed_latest_price = live_quote.get("price")
    if displayed_latest_price in (None, 0):
        displayed_latest_price = latest_price["close"] if latest_price["close"] is not None else 0

    displayed_latest_price_date = live_quote.get("date") or latest_price["price_date"] or "N/A"

    latest_price_judgment = build_latest_price_judgment(
        latest_price=displayed_latest_price,
        latest_price_date=displayed_latest_price_date,
        ma20=ma20,
        fair_value=fair_value,
        base_suggestion=score_report.get("investment_suggestion") or old_valuation["investment_suggestion"],
        base_reason=score_report.get("reason") or old_valuation["reason"],
    )

    report = {
        "symbol": symbol,
        "company_name": overview["company_name"],
        "latest_price": displayed_latest_price if displayed_latest_price is not None else 0,
        "latest_price_date": displayed_latest_price_date,
        "latest_price_source": live_quote.get("source", "finmind"),
        "latest_spread": latest_price["spread"] if latest_price["spread"] is not None else 0,
        "enterprise_overview": {
            "industry_category": overview["industry_category"],
            "main_products_services": overview["main_products_services"],
            "market_position": overview["market_position"]
        },
        "financial_performance": {
            "revenue_trend_3y": rev3y,
            "gross_margin": format_pct(gross_margin),
            "roe": format_pct(roe),
            "debt_ratio": format_pct(debt_ratio),
            "debt_to_equity": format_ratio(debt_to_equity),
            "trailing_pe": format_ratio(latest_price["per"]),
            "pbr": format_ratio(latest_price["pbr"]),
        },
        "competitive_advantage": moat,
        "risk_assessment": risk,
        "price_analysis": price_analysis,
        "news_analysis": news_analysis,
        "valuation": {
            "news_score": news_score,
            "trailing_pe": format_ratio(latest_price["per"]),
            "pe_range": fair_pe_range if fair_pe_range != "N/A" else old_valuation["pe_range"],
            "fair_value": fair_value if fair_value is not None else 0,
            "ma20": ma20 if ma20 is not None else 0,
            "score": blended_total_score,
            "valuation_score": safe_int(score_report.get("valuation_score", 0), 0),
            "quality_score": safe_int(score_report.get("quality_score", 0), 0),
            "growth_score": safe_int(score_report.get("growth_score", 0), 0),
            "technical_score": safe_int(score_report.get("technical_score", 0), 0),
            "investment_suggestion": latest_price_judgment["suggestion"],
            "latest_signal_reason": latest_price_judgment["signal_reason"],
            "reason": latest_price_judgment["reason"],
        }
    }

    report.setdefault("latest_price", 0)

    valuation = report.get("valuation", {})
    if not isinstance(valuation, dict):
        valuation = {}

    valuation.setdefault("score", 0)
    valuation.setdefault("fair_value", 0)
    valuation.setdefault("ma20", 0)
    valuation.setdefault("investment_suggestion", "適合")
    valuation.setdefault("news_score", 10)
    valuation.setdefault("latest_signal_reason", "")

    report["valuation"] = valuation

    return report
