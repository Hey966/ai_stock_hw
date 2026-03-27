import json
import paho.mqtt.publish as publish

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "ai_stock_demo_966/alerts"

message = {
    "symbol": "2330",
    "signal": "SELL",
    "reason": "價格跌破 MA20，短線轉弱"
}

publish.single(
    TOPIC,
    payload=json.dumps(message, ensure_ascii=False),
    hostname=BROKER,
    port=PORT
)

print("MQTT 訊息已送出")
print("Topic:", TOPIC)
print("內容:", message)
