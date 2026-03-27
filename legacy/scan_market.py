import json
import time
from datetime import datetime
from tw_stock_fundamental import build_structured_report
from analysis_tools import finmind_get


def get_all_tw_stock_symbols():
    rows = finmind_get("TaiwanStockInfo")
    symbols = []

    for r in rows:
        stock_id = str(r.get("stock_id", "")).strip()
        stock_name = str(r.get("stock_name", "")).strip()
        industry = str(r.get("industry_category", "")).strip()

        if not (stock_id.isdigit() and len(stock_id) == 4):
            continue

        if "ETF" in stock_name.upper():
            continue
        if "ETN" in stock_name.upper():
            continue
        if industry in ["ETF", "ETN", "Index", "大盤"]:
            continue

        symbols.append(stock_id)

    return sorted(list(set(symbols)))


def classify_market():
    symbols = get_all_tw_stock_symbols()[:80]

    result = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "suitable": [],
        "buy": [],
        "hold": [],
        "sell": [],
        "failed": []
    }

    success_count = 0
    fail_count = 0
    total = len(symbols)

    for idx, symbol in enumerate(symbols, start=1):
        success = False
        last_error = ""

        for attempt in range(3):
            try:
                report = build_structured_report(symbol)
                valuation = report.get("valuation", {})
                suggestion = str(valuation.get("investment_suggestion", "")).strip()

                item = {
                    "symbol": report.get("symbol", symbol),
                    "company_name": report.get("company_name", symbol),
                    "suggestion": suggestion or "適合"
                }

                if suggestion == "買入":
                    result["buy"].append(item)
                elif suggestion == "持有":
                    result["hold"].append(item)
                elif suggestion == "賣出":
                    result["sell"].append(item)
                else:
                    result["suitable"].append(item)

                success_count += 1
                success = True
                print(f"[OK] {symbol} 完成 ({idx}/{total})")
                break

            except Exception as e:
                last_error = str(e)
                time.sleep(1.2 * (attempt + 1))

        if not success:
            fail_count += 1
            result["failed"].append({
                "symbol": symbol,
                "error": last_error
            })
            print(f"[SKIP] {symbol} 失敗：{last_error}")

        time.sleep(1.0)

    with open("market_scan_cache.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("✅ 已完成全市場分類")
    print(f"成功: {success_count}")
    print(f"失敗: {fail_count}")
    print(f"適合區: {len(result['suitable'])}")
    print(f"買入區: {len(result['buy'])}")
    print(f"持有區: {len(result['hold'])}")
    print(f"賣出區: {len(result['sell'])}")
    print("✅ 已輸出 market_scan_cache.json")


if __name__ == "__main__":
    classify_market()