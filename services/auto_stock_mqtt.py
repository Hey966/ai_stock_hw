import os
import json
import time
import requests
import paho.mqtt.publish as publish

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "ai_stock_demo_966/alerts"

CHECK_INTERVAL = 60
stocks = ["2330", "2317", "2603"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
RESULT_FILE = os.path.join(PROJECT_ROOT, "latest_results.json")

last_sent_signals = {}
latest_results = {}


def get_stock_data(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.TW?range=1mo&interval=1d"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=10)
    if res.status_code != 200:
        raise Exception(f"HTTP 錯誤: {res.status_code}")

    data = res.json()
    chart = data.get("chart", {})
    result = chart.get("result")

    if not result or not isinstance(result, list):
        error_info = chart.get("error")
        raise Exception(f"找不到 chart.result 資料，error={error_info}")

    result0 = result[0]
    meta = result0.get("meta", {})
    indicators = result0.get("indicators", {}).get("quote", [{}])[0]

    price = meta.get("regularMarketPrice")
    opens_raw = indicators.get("open", [])
    highs_raw = indicators.get("high", [])
    lows_raw = indicators.get("low", [])
    closes_raw = indicators.get("close", [])
    timestamps = result0.get("timestamp", [])

    if price is None:
        raise Exception("找不到目前價格")

    candles = []
    closes_for_ma = []

    for i in range(min(len(timestamps), len(opens_raw), len(highs_raw), len(lows_raw), len(closes_raw))):
        o = opens_raw[i]
        h = highs_raw[i]
        l = lows_raw[i]
        c = closes_raw[i]

        if None in (o, h, l, c):
            continue

        label = time.strftime("%m/%d", time.localtime(timestamps[i]))
        candles.append({
            "x": label,
            "o": round(float(o), 2),
            "h": round(float(h), 2),
            "l": round(float(l), 2),
            "c": round(float(c), 2),
        })
        closes_for_ma.append(float(c))

    if len(closes_for_ma) < 20:
        raise Exception("歷史收盤價不足 20 筆")

    recent_candles = candles[-20:]
    recent_closes = closes_for_ma[-20:]
    labels = [x["x"] for x in recent_candles]

    ma20 = sum(closes_for_ma[-20:]) / 20
    prev_close = closes_for_ma[-2] if len(closes_for_ma) >= 2 else price
    change_percent = ((price - prev_close) / prev_close) * 100 if prev_close else 0

    return (
        float(price),
        float(ma20),
        float(change_percent),
        labels,
        recent_closes,
        recent_candles
    )


def generate_ai_advice(symbol, price, ma20, fair_value, signal, change_percent):
    if signal == "BUY":
        return f"AI判斷：{symbol} 目前價格 {price:.2f} 低於估計合理價 {fair_value:.2f}，近一日漲跌 {change_percent:.2f}%，可考慮分批布局，但仍需注意市場波動。"
    elif signal == "SELL":
        return f"AI判斷：{symbol} 目前價格 {price:.2f} 已跌破 MA20 {ma20:.2f}，近一日漲跌 {change_percent:.2f}%，短線趨勢偏弱，建議保守操作或分批減碼。"
    else:
        return f"AI判斷：{symbol} 目前價格 {price:.2f} 仍在觀察區間，近一日漲跌 {change_percent:.2f}%，建議持續觀察。"


def analyze(symbol):
    price, ma20, change_percent, labels, chart_data, candles = get_stock_data(symbol)

    fair_value = ma20 * 0.95

    if price < ma20 and price > fair_value:
        signal = "SELL"
        reason = "目前價格跌破真實 MA20，短線轉弱"
    elif price < fair_value:
        signal = "BUY"
        reason = "目前價格低於估計合理價"
    else:
        signal = "HOLD"
        reason = "價格仍在合理區間，暫時觀望"

    ai_advice = generate_ai_advice(symbol, price, ma20, fair_value, signal, change_percent)

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "ma20": round(ma20, 2),
        "fair_value": round(fair_value, 2),
        "change_percent": round(change_percent, 2),
        "signal": signal,
        "reason": reason,
        "ai_advice": ai_advice,
        "chart_labels": labels,
        "chart_data": [round(x, 2) for x in chart_data],
        "candles": candles
    }


def send_mqtt_message(data):
    publish.single(
        TOPIC,
        payload=json.dumps(data, ensure_ascii=False),
        hostname=BROKER,
        port=PORT
    )


def save_results_to_file():
    try:
        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            json.dump(list(latest_results.values()), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("儲存 latest_results.json 失敗:", e)


def main():
    print("📈 AI 股票監控系統啟動")
    print(f"每 {CHECK_INTERVAL} 秒更新\n")

    while True:
        for symbol in stocks:
            try:
                result = analyze(symbol)
                latest_results[symbol] = result
                print(result)

                signal = result["signal"]
                if signal in ["BUY", "SELL"]:
                    if last_sent_signals.get(symbol) != signal:
                        send_mqtt_message(result)
                        last_sent_signals[symbol] = signal
                        print(f"🚀 發送通知: {symbol} {signal}")
                    else:
                        print(f"略過重複通知: {symbol}")
                else:
                    print(f"{symbol} HOLD，不發送通知")

            except Exception as e:
                print(f"錯誤 ({symbol}): {e}")

        save_results_to_file()
        print("\n⏳ 等待下一輪...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()