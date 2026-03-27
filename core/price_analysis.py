def analyze_price_structure(price_rows):
    if not price_rows or len(price_rows) < 30:
        return {
            "trend": "unknown",
            "volatility": 0,
            "momentum": 0,
            "score": 0
        }

    closes = [float(r["close"]) for r in price_rows if r.get("close")]

    latest = closes[-1]
    ma20 = sum(closes[-20:]) / 20
    ma60 = sum(closes[-60:]) / 60 if len(closes) >= 60 else ma20

    # 趨勢判斷
    if latest > ma20 > ma60:
        trend = "strong_up"
        trend_score = 30
    elif latest > ma20:
        trend = "up"
        trend_score = 20
    elif latest < ma20 < ma60:
        trend = "down"
        trend_score = 5
    else:
        trend = "weak"
        trend_score = 10

    # 波動
    returns = []
    for i in range(1, len(closes)):
        returns.append((closes[i] - closes[i-1]) / closes[i-1])

    volatility = sum([abs(r) for r in returns[-20:]]) / 20

    # 動能
    momentum = (latest - closes[-20]) / closes[-20]

    score = trend_score

    if momentum > 0.1:
        score += 10
    elif momentum < -0.1:
        score -= 10

    if volatility > 0.03:
        score -= 5

    return {
        "trend": trend,
        "volatility": round(volatility, 4),
        "momentum": round(momentum, 4),
        "score": max(0, min(score, 40))
    }