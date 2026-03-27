import math
from collections import defaultdict
import requests
from .finmind_auth import get_finmind_token

BASE_URL = "https://api.finmindtrade.com/api/v4/data"


def finmind_get(dataset: str, **params):
    headers = {"Authorization": f"Bearer {get_finmind_token()}"}
    query = {"dataset": dataset}
    query.update(params)

    resp = requests.get(BASE_URL, headers=headers, params=query, timeout=20)
    if resp.status_code != 200:
        raise Exception(f"FinMind API 錯誤: {resp.status_code}")

    data = resp.json()
    if "data" not in data:
        raise Exception(f"FinMind 回傳格式異常: {data}")

    return data["data"]


def safe_float(v, default=None):
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


# =========================
# 1. 風險管理模組
# =========================

def get_stock_price_history(symbol: str, start_date="2024-01-01"):
    rows = finmind_get("TaiwanStockPrice", data_id=symbol, start_date=start_date)
    rows = [r for r in rows if r.get("close") is not None]
    rows = sorted(rows, key=lambda x: x["date"])
    return rows


def calc_daily_returns(price_rows):
    closes = [safe_float(r["close"]) for r in price_rows if r.get("close") is not None]
    returns = []
    for i in range(1, len(closes)):
        prev_p = closes[i - 1]
        cur_p = closes[i]
        if prev_p and prev_p != 0:
            returns.append((cur_p - prev_p) / prev_p)
    return returns


def percentile(sorted_list, p):
    if not sorted_list:
        return None
    k = (len(sorted_list) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_list[int(k)]
    d0 = sorted_list[f] * (c - k)
    d1 = sorted_list[c] * (k - f)
    return d0 + d1


def calc_var_cvar(returns, confidence=0.95):
    if not returns:
        return None, None

    sorted_r = sorted(returns)
    cutoff = percentile(sorted_r, 1 - confidence)
    var_95 = abs(cutoff)

    tail_losses = [r for r in sorted_r if r <= cutoff]
    if not tail_losses:
        cvar_95 = var_95
    else:
        cvar_95 = abs(sum(tail_losses) / len(tail_losses))

    return var_95, cvar_95


def calc_max_drawdown(returns):
    if not returns:
        return None

    nav = 1.0
    peak = 1.0
    max_dd = 0.0

    for r in returns:
        nav *= (1 + r)
        if nav > peak:
            peak = nav
        dd = (nav - peak) / peak
        if dd < max_dd:
            max_dd = dd

    return abs(max_dd)


def normalize_weights(positions):
    total = sum([safe_float(p.get("weight"), 0) for p in positions])
    if total == 0:
        raise Exception("投資組合權重總和不能為 0")

    result = []
    for p in positions:
        w = safe_float(p.get("weight"), 0) / total
        result.append({
            "symbol": str(p["symbol"]).strip(),
            "weight": w
        })
    return result


def merge_portfolio_returns(positions, start_date="2024-01-01"):
    positions = normalize_weights(positions)

    all_series = {}
    min_len = None

    for p in positions:
        symbol = p["symbol"]
        rows = get_stock_price_history(symbol, start_date=start_date)
        rets = calc_daily_returns(rows)

        if len(rets) < 30:
            raise Exception(f"{symbol} 歷史資料不足，無法進行風險分析")

        all_series[symbol] = rets
        if min_len is None or len(rets) < min_len:
            min_len = len(rets)

    portfolio_returns = []
    for i in range(min_len):
        day_r = 0
        for p in positions:
            symbol = p["symbol"]
            day_r += all_series[symbol][-min_len + i] * p["weight"]
        portfolio_returns.append(day_r)

    return portfolio_returns


def get_stock_info_map():
    rows = finmind_get("TaiwanStockInfo")
    info_map = {}
    for r in rows:
        info_map[str(r.get("stock_id"))] = r
    return info_map


def analyze_portfolio_risk(positions, benchmark="0050", factors=""):
    positions = normalize_weights(positions)
    info_map = get_stock_info_map()

    portfolio_returns = merge_portfolio_returns(positions)
    var_95, cvar_95 = calc_var_cvar(portfolio_returns, confidence=0.95)
    mdd = calc_max_drawdown(portfolio_returns)

    exposure = []
    industry_weights = defaultdict(float)

    for p in positions:
        symbol = p["symbol"]
        info = info_map.get(symbol, {})
        stock_name = info.get("stock_name", symbol)
        industry = info.get("industry_category", "未知產業")
        w = p["weight"]

        exposure.append({
            "symbol": symbol,
            "name": stock_name,
            "industry": industry,
            "weight": round(w * 100, 2)
        })
        industry_weights[industry] += w

    stock_concentration = sorted(
        exposure, key=lambda x: x["weight"], reverse=True
    )

    industry_concentration = sorted(
        [{"industry": k, "weight": round(v * 100, 2)} for k, v in industry_weights.items()],
        key=lambda x: x["weight"],
        reverse=True
    )

    risk_advice = []
    if var_95 is not None and var_95 > 0.03:
        risk_advice.append("VaR 偏高，建議降低高波動部位或分散持股。")
    if cvar_95 is not None and cvar_95 > 0.04:
        risk_advice.append("CVaR 顯示尾部損失風險偏大，建議加入防禦型資產或避險工具。")
    if mdd is not None and mdd > 0.2:
        risk_advice.append("最大回檔偏大，建議降低集中度並設定停損或再平衡機制。")
    if stock_concentration and stock_concentration[0]["weight"] > 40:
        risk_advice.append("單一個股權重過高，建議減持以降低集中度風險。")
    if industry_concentration and industry_concentration[0]["weight"] > 50:
        risk_advice.append("產業集中度過高，建議增加跨產業配置。")

    if not risk_advice:
        risk_advice.append("目前風險結構尚可，建議維持現狀並定期檢查波動與集中度。")

    return {
        "positions": stock_concentration,
        "industry_concentration": industry_concentration,
        "quant_metrics": {
            "VaR_95": f"{var_95 * 100:.2f}%" if var_95 is not None else "N/A",
            "CVaR_95": f"{cvar_95 * 100:.2f}%" if cvar_95 is not None else "N/A",
            "max_drawdown": f"{mdd * 100:.2f}%" if mdd is not None else "N/A",
        },
        "benchmark": benchmark,
        "factors": factors,
        "risk_advice": risk_advice
    }


# =========================
# 2. 產業分析模組
# =========================

def analyze_industry(target, benchmark="", factors=""):
    target = str(target).strip()

    industry_map = {
        "半導體": {
            "market_size": "全球半導體市場規模龐大，長期受 AI、HPC、車用電子與先進製程需求驅動。",
            "growth": "中長期成長動能來自 AI 晶片、先進封裝、資料中心與邊緣運算。",
            "value_chain": "上游：矽晶圓 / 設備 / 材料；中游：IC 設計 / 晶圓代工 / 封測；下游：品牌廠 / 系統整合 / 終端應用。",
            "competition": "主要業者常見於 IC 設計、晶圓代工、封測與設備供應鏈，各自具有分工優勢。",
            "drivers": "AI、先進製程、資料中心擴張、車用與高效能運算。",
            "challenges": "景氣循環、庫存調整、地緣政治、資本支出壓力。",
            "ideas": "值得關注：2330、2303、3711，或半導體 ETF。"
        },
        "航運": {
            "market_size": "航運市場受全球貿易量、運價與供需循環影響。",
            "growth": "成長性受全球景氣、運價與船舶供給控制。",
            "value_chain": "上游：造船 / 燃油；中游：貨櫃航運 / 散裝航運；下游：物流 / 港口 / 終端出口商。",
            "competition": "競爭格局常由大型船隊與全球航線能力主導。",
            "drivers": "全球貿易復甦、運價上升、供給調整。",
            "challenges": "景氣循環、油價、地緣衝突與供需失衡。",
            "ideas": "值得關注：2603、2615、2610。"
        },
        "電子": {
            "market_size": "電子產業規模廣泛，涵蓋消費電子、通訊、網通、伺服器與零組件。",
            "growth": "AI 伺服器、邊緣裝置、雲端建設與升級需求帶動成長。",
            "value_chain": "上游：材料 / 零件；中游：組裝 / 模組 / 代工；下游：品牌與終端應用。",
            "competition": "競爭重點在規模、成本控制、良率與客戶認證。",
            "drivers": "AI、雲端、企業資本支出、產品升級週期。",
            "challenges": "毛利率壓力、價格競爭、需求波動。",
            "ideas": "值得關注：2317、2382、3231，或電子 ETF。"
        }
    }

    data = industry_map.get(target, {
        "market_size": f"{target} 產業可進一步補充市場規模資料。",
        "growth": f"{target} 產業成長預測需搭配研究報告或統計資料更新。",
        "value_chain": f"{target} 產業價值鏈可拆解為上中下游結構。",
        "competition": f"{target} 產業競爭格局需依主要業者與市占率整理。",
        "drivers": f"{target} 產業成長動能需視政策、技術、需求與資本支出而定。",
        "challenges": f"{target} 產業需留意競爭、景氣與法規變化。",
        "ideas": f"{target} 產業可進一步篩選代表性個股或 ETF。"
    })

    return {
        "target": target,
        "benchmark": benchmark,
        "factors": factors,
        "industry_overview": {
            "market_size_and_growth": f"{data['market_size']} {data['growth']}"
        },
        "value_chain": data["value_chain"],
        "competition": data["competition"],
        "drivers_and_challenges": {
            "drivers": data["drivers"],
            "challenges": data["challenges"]
        },
        "investment_ideas": data["ideas"]
    }


# =========================
# 3. 固定收益分析模組
# =========================

def calc_nominal_yield(coupon_rate, face_value, price):
    annual_coupon = coupon_rate * face_value
    return annual_coupon / price


def calc_ytm_approx(coupon_rate, face_value, price, years_to_maturity):
    annual_coupon = coupon_rate * face_value
    return (annual_coupon + (face_value - price) / years_to_maturity) / ((face_value + price) / 2)


def analyze_fixed_income(
    target_name,
    benchmark="",
    factors="",
    price=100,
    face_value=100,
    coupon_rate=0.03,
    years_to_maturity=5,
    credit_rating="A"
):
    nominal_yield = calc_nominal_yield(coupon_rate, face_value, price)
    ytm = calc_ytm_approx(coupon_rate, face_value, price, years_to_maturity)

    risk_note = {
        "AAA": "信用風險低，違約風險相對有限。",
        "AA": "信用風險偏低，具穩定性。",
        "A": "信用風險中等，需觀察發行人財務狀況。",
        "BBB": "接近投資等級下緣，需留意景氣反轉風險。",
        "BB": "非投資等級，違約風險較高。"
    }.get(credit_rating, "請自行補充信用評等風險說明。")

    advice = "殖利率吸引力中性，建議與同天期公債或投資等級債比較。"
    if ytm > 0.06:
        advice = "殖利率相對具吸引力，但需特別檢查信用風險與流動性。"
    elif ytm < 0.03:
        advice = "殖利率吸引力偏低，除非防禦需求明確，否則吸引力有限。"

    return {
        "target_name": target_name,
        "benchmark": benchmark,
        "factors": factors,
        "nominal_yield": f"{nominal_yield * 100:.2f}%",
        "ytm": f"{ytm * 100:.2f}%",
        "credit_rating": credit_rating,
        "credit_risk_note": risk_note,
        "peer_comparison_note": f"建議與 {benchmark or '同類固定收益商品或指數'} 比較殖利率與信用風險。",
        "investment_advice": advice
    }