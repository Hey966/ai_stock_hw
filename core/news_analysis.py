import os
import time
import requests
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

NEWSAPI_URL = "https://newsapi.org/v2/everything"
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"

NEWS_CACHE = {}
NEWS_CACHE_TTL = 60 * 30  # 30 分鐘


POSITIVE_KEYWORDS = [
    "成長", "創高", "擴產", "利多", "上修", "調升", "買進", "看好", "突破",
    "合作", "訂單", "增產", "受惠", "回溫", "強勁", "優於預期", "獲利成長",
    "營收成長", "AI", "法說利多", "新產品", "市占提升", "利潤改善"
]

NEGATIVE_KEYWORDS = [
    "下滑", "衰退", "利空", "調降", "賣出", "跌破", "虧損", "裁員", "砍單",
    "違約", "訴訟", "風險", "衝擊", "庫存", "疲弱", "不如預期", "營收下滑",
    "獲利下滑", "地緣政治", "關稅", "事故", "停工", "停產", "下修"
]


def _now_ts():
    return time.time()


def _cache_get(key):
    data = NEWS_CACHE.get(key)
    if not data:
        return None
    if _now_ts() - data["ts"] > NEWS_CACHE_TTL:
        return None
    return data["value"]


def _cache_set(key, value):
    NEWS_CACHE[key] = {
        "ts": _now_ts(),
        "value": value,
    }


def _safe_text(v, default=""):
    if v is None:
        return default
    return str(v).strip()


def _build_queries(symbol: str, company_name: str, industry: str):
    queries = []
    symbol = _safe_text(symbol)
    company_name = _safe_text(company_name)
    industry = _safe_text(industry)

    if company_name and company_name != symbol:
        queries.append(company_name)
    if symbol:
        queries.append(symbol)
    if company_name and symbol and company_name != symbol:
        queries.append(f"{company_name} {symbol}")
    if industry and industry != "N/A":
        queries.append(f"{company_name} {industry}".strip())

    seen = set()
    result = []
    for q in queries:
        if q and q not in seen:
            seen.add(q)
            result.append(q)
    return result[:4]


def _score_text(text: str):
    text = _safe_text(text)
    if not text:
        return 0

    score = 0
    for kw in POSITIVE_KEYWORDS:
        if kw in text:
            score += 1

    for kw in NEGATIVE_KEYWORDS:
        if kw in text:
            score -= 1

    return score


def _normalize_news_item(title, source, published_at, url, summary=""):
    return {
        "title": _safe_text(title),
        "source": _safe_text(source, "Unknown"),
        "published_at": _safe_text(published_at),
        "url": _safe_text(url),
        "summary": _safe_text(summary),
    }


def _fetch_from_newsapi(query: str, days: int = 7, page_size: int = 10):
    api_key = os.getenv("NEWSAPI_KEY", "").strip()
    if not api_key:
        return []

    from_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    params = {
        "q": query,
        "language": "zh",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "from": from_date,
        "apiKey": api_key,
    }

    resp = requests.get(NEWSAPI_URL, params=params, timeout=20)
    if resp.status_code != 200:
        return []

    payload = resp.json()
    articles = payload.get("articles", [])

    result = []
    for a in articles:
        result.append(
            _normalize_news_item(
                title=a.get("title"),
                source=(a.get("source") or {}).get("name", ""),
                published_at=a.get("publishedAt", ""),
                url=a.get("url", ""),
                summary=a.get("description", ""),
            )
        )
    return result


def _fetch_from_google_rss(query: str, max_items: int = 10):
    rss_url = GOOGLE_NEWS_RSS.format(query=quote_plus(query))
    try:
        resp = requests.get(rss_url, timeout=20)
        if resp.status_code != 200:
            return []
    except Exception:
        return []

    try:
        root = ET.fromstring(resp.text)
    except Exception:
        return []

    result = []
    for item in root.findall(".//item")[:max_items]:
        title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        pub_date = item.findtext("pubDate", default="")
        source = "Google News RSS"

        try:
            pub_date = parsedate_to_datetime(pub_date).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

        result.append(
            _normalize_news_item(
                title=title,
                source=source,
                published_at=pub_date,
                url=link,
                summary="",
            )
        )
    return result


def _dedupe_news(items):
    seen = set()
    result = []
    for item in items:
        key = (item["title"], item["url"])
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _calc_news_result(symbol: str, company_name: str, industry: str, items):
    headline_count = len(items)

    total_text_score = 0
    positive_count = 0
    negative_count = 0

    for item in items:
        text = f"{item.get('title', '')} {item.get('summary', '')}"
        s = _score_text(text)
        total_text_score += s
        if s > 0:
            positive_count += 1
        elif s < 0:
            negative_count += 1

    if headline_count == 0:
        sentiment_score = 0
    else:
        sentiment_score = round(total_text_score / headline_count, 2)

    # 轉成 0~20 分的新聞分數
    news_score = 10
    if sentiment_score >= 1.0:
        news_score = 18
    elif sentiment_score >= 0.5:
        news_score = 15
    elif sentiment_score > 0:
        news_score = 12
    elif sentiment_score == 0:
        news_score = 10
    elif sentiment_score > -0.5:
        news_score = 7
    elif sentiment_score > -1.0:
        news_score = 4
    else:
        news_score = 1

    if headline_count >= 8 and sentiment_score > 0:
        news_score = min(20, news_score + 1)

    if negative_count >= 3 and sentiment_score < 0:
        risk_level = "高"
    elif negative_count >= 1:
        risk_level = "中"
    else:
        risk_level = "低"

    if headline_count == 0:
        summary = f"近 7 天未抓到 {company_name or symbol} 相關新聞，新聞分數採中性處理。"
    else:
        summary = (
            f"近 7 天共抓到 {headline_count} 則相關新聞；"
            f"偏多 {positive_count}、偏空 {negative_count}，"
            f"新聞情緒分數 {sentiment_score}，事件風險 {risk_level}。"
        )

    return {
        "symbol": symbol,
        "company_name": company_name,
        "headline_count": headline_count,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "sentiment_score": sentiment_score,
        "news_score": news_score,
        "risk_level": risk_level,
        "summary": summary,
        "top_news": items[:5],
    }


def analyze_stock_news(symbol: str, company_name: str = "", industry: str = ""):
    cache_key = f"{symbol}|{company_name}|{industry}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    queries = _build_queries(symbol, company_name, industry)
    all_items = []

    # 先走 NewsAPI
    for q in queries:
        items = _fetch_from_newsapi(q, days=7, page_size=8)
        all_items.extend(items)

    # NewsAPI 沒抓到，再走 RSS 備援
    if not all_items:
        for q in queries:
            items = _fetch_from_google_rss(q, max_items=8)
            all_items.extend(items)

    all_items = _dedupe_news(all_items)

    result = _calc_news_result(
        symbol=symbol,
        company_name=company_name,
        industry=industry,
        items=all_items,
    )

    _cache_set(cache_key, result)
    return result