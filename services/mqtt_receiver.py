import json
import subprocess
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "ai_stock_demo_966/alerts"

STOCK_NAMES = {
    "2330": "台積電",
    "2317": "鴻海",
    "2603": "長榮",
}


def send_notification(title, content):
    try:
        subprocess.run(
            [
                "termux-notification",
                "--title", title,
                "--content", content
            ],
            check=False
        )
    except Exception as e:
        print("通知錯誤:", e)


def on_connect(client, userdata, flags, rc):
    print("已連線到 MQTT Broker")
    client.subscribe(TOPIC)
    print("已訂閱 Topic:", TOPIC)


def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print("\n收到訊息:")
    print(text)

    try:
        data = json.loads(text)

        symbol = str(data.get("symbol", "未知"))
        stock_name = STOCK_NAMES.get(symbol, "未知股票")
        signal = data.get("signal", "未知")
        reason = data.get("reason", "無說明")
        price = data.get("price", "未知")
        change = data.get("change_percent", 0)
        ai_advice = data.get("ai_advice", "無 AI 建議")

        if signal == "BUY":
            title = f"📈 {stock_name} ({symbol})"
        elif signal == "SELL":
            title = f"📉 {stock_name} ({symbol})"
        else:
            title = f"ℹ️ {stock_name} ({symbol})"

        content = f"價格：{price}\n漲跌：{change}%\n訊號：{signal}\n原因：{reason}\n{ai_advice}"

        send_notification(title, content)

    except Exception:
        send_notification("📢 股票通知", text)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()