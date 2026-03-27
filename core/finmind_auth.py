import os
import time
import requests

LOGIN_URL = "https://api.finmindtrade.com/api/v4/login"

_token_cache = {
    "token": None,
    "ts": 0
}

TOKEN_TTL_SECONDS = 60 * 60 * 6  # 6小時內重用一次，避免每次都重新登入


def get_finmind_token():
    now = time.time()

    if _token_cache["token"] and now - _token_cache["ts"] < TOKEN_TTL_SECONDS:
        return _token_cache["token"]

    email = os.getenv("FINMIND_EMAIL", "").strip()
    password = os.getenv("FINMIND_PASSWORD", "").strip()

    if not email or not password:
        raise Exception("請先設定 FINMIND_EMAIL 與 FINMIND_PASSWORD 環境變數。")

    payload = {
        "user_id": email,
        "password": password
    }

    resp = requests.post(LOGIN_URL, data=payload, timeout=20)

    if resp.status_code != 200:
        raise Exception(f"FinMind 登入失敗，狀態碼: {resp.status_code}")

    data = resp.json()

    if "token" not in data:
        raise Exception(f"FinMind 未回傳 token，內容: {data}")

    token = data["token"]
    _token_cache["token"] = token
    _token_cache["ts"] = now
    return token