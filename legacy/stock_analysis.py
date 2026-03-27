stocks = [
    {"symbol": "2330", "price": 1800, "ma20": 1895, "fair_value": 1620},
    {"symbol": "2317", "price": 120, "ma20": 115, "fair_value": 130},
    {"symbol": "2603", "price": 210, "ma20": 205, "fair_value": 220},
    {"symbol": "0050", "price": 165, "ma20": 168, "fair_value": 172},
]

def analyze(stock):
    price = stock["price"]
    ma20 = stock["ma20"]
    fair_value = stock["fair_value"]

    if price < ma20 and price > fair_value:
        signal = "SELL"
        reason = "價格跌破 MA20，短線轉弱，且目前仍高於合理價"
    elif price < fair_value:
        signal = "BUY"
        reason = "價格低於合理價，具有投資吸引力"
    else:
        signal = "HOLD"
        reason = "目前價格介於技術面與估值之間，建議觀望"

    return {
        "symbol": stock["symbol"],
        "price": price,
        "ma20": ma20,
        "fair_value": fair_value,
        "signal": signal,
        "reason": reason
    }

def main():
    print("=== AI 股票分析結果 ===\n")
    for stock in stocks:
        result = analyze(stock)
        print(f"股票代號: {result['symbol']}")
        print(f"現價: {result['price']}")
        print(f"MA20: {result['ma20']}")
        print(f"合理價: {result['fair_value']}")
        print(f"建議: {result['signal']}")
        print(f"原因: {result['reason']}")
        print("-" * 30)

if __name__ == "__main__":
    main()
