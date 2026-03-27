from __future__ import annotations

import pandas as pd

TWSE_ISIN_URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
TPEX_ISIN_URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"


def _parse_isin_table(url: str, suffix: str) -> list[dict]:
    tables = pd.read_html(url, encoding="utf-8")
    if not tables:
        return []

    df = tables[0].copy()
    df.columns = [str(c).strip() for c in df.columns]

    first_col = df.columns[0]
    df = df.rename(columns={first_col: "raw_name"})

    results: list[dict] = []

    for _, row in df.iterrows():
        raw = str(row.get("raw_name", "")).strip()

        if not raw:
            continue

        parts = raw.split()
        if len(parts) < 2:
            continue

        code = parts[0].strip()
        name = " ".join(parts[1:]).strip()

        if not code.isdigit():
            continue

        if len(code) != 4:
            continue

        results.append(
            {
                "symbol": code,
                "name": name,
                "ticker": f"{code}{suffix}",
            }
        )

    return results


def get_tw_stock_universe(include_twse: bool = True, include_tpex: bool = True) -> list[dict]:
    universe: list[dict] = []

    if include_twse:
        universe.extend(_parse_isin_table(TWSE_ISIN_URL, ".TW"))

    if include_tpex:
        universe.extend(_parse_isin_table(TPEX_ISIN_URL, ".TWO"))

    # 去重
    seen = set()
    deduped = []
    for item in universe:
        ticker = item["ticker"]
        if ticker in seen:
            continue
        seen.add(ticker)
        deduped.append(item)

    return deduped