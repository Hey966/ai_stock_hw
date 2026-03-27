def safe_float(v, default=None):
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def score_valuation(latest_price, fair_value, trailing_pe, industry_category=""):
    score = 0
    reason = []

    price = safe_float(latest_price)
    fv = safe_float(fair_value)
    pe = safe_float(trailing_pe)

    if price is not None and fv is not None and fv > 0:
        ratio = price / fv
        if ratio <= 0.85:
            score += 30
            reason.append("股價明顯低於合理價")
        elif ratio <= 1.00:
            score += 22
            reason.append("股價低於或接近合理價")
        elif ratio <= 1.15:
            score += 12
            reason.append("股價略高於合理價")
        else:
            score += 3
            reason.append("股價偏高於合理價")

    # 產業化簡 PE 判斷
    pe_low = 10
    pe_mid = 18
    pe_high = 25

    if "半導體" in industry_category or "電子" in industry_category:
        pe_low = 15
        pe_mid = 25
        pe_high = 35

    if pe is not None:
        if pe <= pe_low:
            score += 15
            reason.append("本益比偏低")
        elif pe <= pe_mid:
            score += 10
            reason.append("本益比合理")
        elif pe <= pe_high:
            score += 5
            reason.append("本益比偏高但可接受")
        else:
            score += 0
            reason.append("本益比偏高")

    return min(score, 40), reason


def score_quality(roe, gross_margin, debt_ratio):
    score = 0
    reason = []

    roe_v = safe_float(roe)
    gm_v = safe_float(gross_margin)
    debt_v = safe_float(debt_ratio)

    if roe_v is not None:
        if roe_v >= 20:
            score += 15
            reason.append("ROE 優秀")
        elif roe_v >= 15:
            score += 12
            reason.append("ROE 良好")
        elif roe_v >= 10:
            score += 8
            reason.append("ROE 穩定")
        else:
            score += 3
            reason.append("ROE 普通")

    if gm_v is not None:
        if gm_v >= 40:
            score += 10
            reason.append("毛利率高")
        elif gm_v >= 25:
            score += 7
            reason.append("毛利率尚可")
        elif gm_v >= 15:
            score += 4
            reason.append("毛利率一般")
        else:
            score += 1
            reason.append("毛利率偏低")

    if debt_v is not None:
        if debt_v <= 30:
            score += 10
            reason.append("負債比健康")
        elif debt_v <= 50:
            score += 6
            reason.append("負債比可控")
        elif debt_v <= 65:
            score += 3
            reason.append("負債比偏高")
        else:
            score += 0
            reason.append("負債比過高")

    return min(score, 35), reason


def score_growth(revenue_trend_3y):
    score = 0
    reason = []

    values = []
    for item in revenue_trend_3y or []:
        rev = item.get("revenue_raw")
        if rev is not None:
            values.append(rev)

    if len(values) >= 3:
        if values[-1] > values[-2] > values[-3]:
            score += 15
            reason.append("近三年營收持續成長")
        elif values[-1] > values[-2]:
            score += 10
            reason.append("近期營收改善")
        elif values[-1] >= values[-3]:
            score += 6
            reason.append("營收大致持平")
        else:
            score += 2
            reason.append("營收呈現下滑")
    elif len(values) >= 2:
        if values[-1] > values[-2]:
            score += 8
            reason.append("營收近期成長")
        else:
            score += 3
            reason.append("營收成長有限")
    else:
        reason.append("營收資料不足")

    return min(score, 15), reason


def score_technical(latest_price, ma20):
    score = 0
    reason = []

    price = safe_float(latest_price)
    ma20_v = safe_float(ma20)

    if price is not None and ma20_v is not None and ma20_v > 0:
        if price > ma20_v * 1.03:
            score += 10
            reason.append("股價站穩 MA20 之上")
        elif price >= ma20_v:
            score += 7
            reason.append("股價位於 MA20 之上")
        elif price >= ma20_v * 0.97:
            score += 4
            reason.append("股價接近 MA20")
        else:
            score += 1
            reason.append("股價弱於 MA20")
    else:
        reason.append("技術面資料不足")

    return min(score, 10), reason


def make_investment_signal(total_score):
    if total_score >= 75:
        return "買入"
    if total_score >= 55:
        return "持有"
    return "賣出"


def build_score_report(
    latest_price,
    fair_value,
    trailing_pe,
    industry_category,
    roe,
    gross_margin,
    debt_ratio,
    revenue_trend_3y,
    ma20
):
    val_score, val_reason = score_valuation(
        latest_price=latest_price,
        fair_value=fair_value,
        trailing_pe=trailing_pe,
        industry_category=industry_category,
    )
    quality_score, quality_reason = score_quality(
        roe=roe,
        gross_margin=gross_margin,
        debt_ratio=debt_ratio,
    )
    growth_score, growth_reason = score_growth(revenue_trend_3y)
    tech_score, tech_reason = score_technical(
        latest_price=latest_price,
        ma20=ma20,
    )

    total_score = val_score + quality_score + growth_score + tech_score
    signal = make_investment_signal(total_score)

    reasons = val_reason + quality_reason + growth_reason + tech_reason

    return {
        "total_score": total_score,
        "valuation_score": val_score,
        "quality_score": quality_score,
        "growth_score": growth_score,
        "technical_score": tech_score,
        "investment_suggestion": signal,
        "reason": "；".join(reasons[:6]),
    }