HOME_TEMPLATE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>台股投資分析平台</title>
  {{ base_style|safe }}
</head>
<body>
  <div class="container">
    <div class="nav nav-home">
      <a href="/">首頁</a>
      <a href="/stock?symbol=2330">個股分析</a>
      <a href="/market">市場掃描</a>
      <a href="/daily">今日策略</a>
      <a href="/tools">進階分析工具</a>
    </div>

    <section class="landing-hero">
      <div class="landing-badge">台股投資分析平台</div>
      <h1>把個股研究、盤勢掃描與每日重點放在同一個首頁</h1>
      <p class="landing-subtitle">
        以更清楚的方式整理市場快照、個股查詢與每日策略。
        先看整體盤勢，再回到單一股票做判斷，讓操作流程更一致。
      </p>

      <div class="landing-actions">
        <a class="cta-primary" href="/stock?symbol=2330">查詢個股</a>
        <a class="cta-secondary" href="/market">查看市場掃描</a>
      </div>

      <div class="status-grid" style="margin-top: 18px;">
        <div class="status-pill">
          <div class="status-label">市場更新</div>
          <div class="status-value" id="hero-market-updated-at">
            {{ market_sections.get("updated_at", "N/A") }}
          </div>
        </div>
        <div class="status-pill">
          <div class="status-label">今日策略</div>
          <div class="status-value" id="hero-daily-updated-at">
            {{ daily_selection.get("updated_at", "尚未產生") }}
          </div>
        </div>
        <div class="status-pill">
          <div class="status-label">分析日期</div>
          <div class="status-value" id="hero-daily-date">
            {{ daily_selection.get("date", "尚未產生") }}
          </div>
        </div>
      </div>

      <div class="search-box" style="margin-top: 18px;">
        <form method="get" action="/stock">
          <div class="search-row">
            <input
              type="text"
              name="symbol"
              placeholder="輸入股票代號，例如 2330、2317、2454、0050"
              required
            >
            <button type="submit">開始查詢</button>
          </div>
        </form>
      </div>
    </section>

    <section class="card landing-summary-card">
      <h2 class="section-title"><span class="section-num">1</span>市場與策略摘要</h2>
      <div class="landing-summary-grid">
        <div class="summary-bubble bubble-green">
          <div class="summary-bubble-label">買入區</div>
          <div class="summary-bubble-value" id="home-market-buy-count">
            {{ market_sections.get("buy_count", market_sections.get("buy", [])|length) }}
          </div>
        </div>

        <div class="summary-bubble bubble-yellow">
          <div class="summary-bubble-label">持有區</div>
          <div class="summary-bubble-value" id="home-market-hold-count">
            {{ market_sections.get("hold_count", market_sections.get("hold", [])|length) }}
          </div>
        </div>

        <div class="summary-bubble bubble-red">
          <div class="summary-bubble-label">賣出區</div>
          <div class="summary-bubble-value" id="home-market-sell-count">
            {{ market_sections.get("sell_count", market_sections.get("sell", [])|length) }}
          </div>
        </div>

        <div class="summary-bubble bubble-blue">
          <div class="summary-bubble-label">觀察區</div>
          <div class="summary-bubble-value" id="home-market-watch-count">
            {{ market_sections.get("watch_count", market_sections.get("watch", [])|length) }}
          </div>
        </div>

        <div class="summary-bubble bubble-purple">
          <div class="summary-bubble-label">Top Buy</div>
          <div class="summary-bubble-value" id="home-top-buy-count">
            {{ daily_selection.get("summary", {}).get("top_buy_count", 0) }}
          </div>
        </div>

        <div class="summary-bubble bubble-orange">
          <div class="summary-bubble-label">今日觀察</div>
          <div class="summary-bubble-value" id="home-watch-count">
            {{ daily_selection.get("summary", {}).get("watch_hold_count", 0) }}
          </div>
        </div>

        <div class="summary-bubble bubble-pink">
          <div class="summary-bubble-label">風險名單</div>
          <div class="summary-bubble-value" id="home-risk-count">
            {{ daily_selection.get("summary", {}).get("risk_list_count", 0) }}
          </div>
        </div>
      </div>
    </section>

    <section class="card landing-sync-card">
      <h2 class="section-title"><span class="section-num">2</span>資料更新</h2>
      <div class="status-grid">
        <div class="status-pill">
          <div class="status-label">市場掃描</div>
          <div class="status-value">重新抓取最新市場快取與分類結果</div>
          <div style="margin-top: 12px;">
            <button type="button" onclick="runLatestSync('/api/market-scan/run?limit=20', '正在更新市場掃描，完成後會自動刷新頁面')">
              更新市場掃描
            </button>
          </div>
        </div>

        <div class="status-pill">
          <div class="status-label">今日策略</div>
          <div class="status-value">重新整理 Top Buy、觀察名單與風險名單</div>
          <div style="margin-top: 12px;">
            <button type="button" onclick="runLatestSync('/api/daily-strategy/run?limit=20', '正在更新今日策略，完成後會自動刷新頁面')">
              更新今日策略
            </button>
          </div>
        </div>

        <div class="status-pill">
          <div class="status-label">固定網址</div>
          <div class="status-value">
            <a href="https://app.ai966.online" target="_blank" rel="noopener noreferrer">
              app.ai966.online
            </a>
          </div>
        </div>
      </div>
      <div style="margin-top: 10px; font-size: 14px; color: #667085; line-height: 1.7;">
        需要立即刷新資料時，可直接使用上方按鈕。更新完成後會自動重新整理首頁數據。
      </div>
    </section>

    <section class="feature-showcase">
      <div class="feature-card feature-card-a">
        <div class="feature-icon">📘</div>
        <div class="feature-title">個股分析</div>
        <div class="feature-text">
          從單一股票出發，查看企業概覽、財務指標、估值與新聞重點。
        </div>
        <a href="/stock?symbol=2330">前往個股分析</a>
      </div>

      <div class="feature-card feature-card-b">
        <div class="feature-icon">📡</div>
        <div class="feature-title">市場掃描</div>
        <div class="feature-text">
          用分類方式快速掌握目前盤勢分布，先看全貌，再找標的。
        </div>
        <a href="/market">前往市場掃描</a>
      </div>

      <div class="feature-card feature-card-c">
        <div class="feature-icon">📅</div>
        <div class="feature-title">今日策略</div>
        <div class="feature-text">
          把每日重點整理成 Top Buy、觀察名單與風險名單，方便快速瀏覽。
        </div>
        <a href="/daily">前往今日策略</a>
      </div>

      <div class="feature-card feature-card-d">
        <div class="feature-icon">🧰</div>
        <div class="feature-title">進階工具</div>
        <div class="feature-text">
          針對投資組合、產業與固定收益等主題做進一步分析。
        </div>
        <a href="/tools">前往工具頁</a>
      </div>
    </section>

    <section class="card landing-status-card">
      <h2 class="section-title"><span class="section-num">3</span>系統狀態</h2>
      <div class="status-grid">
        <div class="status-pill">
          <div class="status-label">市場更新</div>
          <div class="status-value" id="home-market-updated-at">
            {{ market_sections.get("updated_at", "N/A") }}
          </div>
        </div>

        <div class="status-pill">
          <div class="status-label">掃描總數</div>
          <div class="status-value" id="home-market-total-scanned">
            {{ market_sections.get("total_scanned", 0) }}
          </div>
        </div>

        <div class="status-pill">
          <div class="status-label">錯誤數量</div>
          <div class="status-value" id="home-market-error-count">
            {{ market_sections.get("error_count", 0) }}
          </div>
        </div>

        <div class="status-pill">
          <div class="status-label">今日策略更新</div>
          <div class="status-value" id="home-daily-updated-at">
            {{ daily_selection.get("updated_at", "尚未產生") }}
          </div>
        </div>

        <div class="status-pill">
          <div class="status-label">分析日期</div>
          <div class="status-value" id="home-daily-date">
            {{ daily_selection.get("date", "尚未產生") }}
          </div>
        </div>
      </div>
    </section>

    <section class="card landing-guide-card">
      <h2 class="section-title"><span class="section-num">4</span>建議使用流程</h2>
      <div class="guide-steps">
        <div class="guide-step">
          <div class="guide-step-no">01</div>
          <div>
            <div class="guide-step-title">先看首頁摘要</div>
            <div class="guide-step-text">快速掌握市場區塊分布與今日策略數量，先建立整體盤勢感。</div>
          </div>
        </div>

        <div class="guide-step">
          <div class="guide-step-no">02</div>
          <div>
            <div class="guide-step-title">再查個股</div>
            <div class="guide-step-text">輸入股票代號，確認基本面、估值、新聞與價格結構。</div>
          </div>
        </div>

        <div class="guide-step">
          <div class="guide-step-no">03</div>
          <div>
            <div class="guide-step-title">需要時再更新資料</div>
            <div class="guide-step-text">若你懷疑資料不是最新，可用同步按鈕立即刷新市場掃描與今日策略。</div>
          </div>
        </div>
      </div>
    </section>

    <div class="footer">AI Stock Dashboard</div>
  </div>

  <script>
    async function runLatestSync(url, loadingMessage) {
      try {
        alert(loadingMessage);
        const response = await fetch(url, { method: "GET" });
        const data = await response.json();

        if (!response.ok || data.status === "error") {
          throw new Error(data.error || "更新失敗");
        }

        alert("更新完成，頁面即將刷新");
        window.location.reload();
      } catch (error) {
        alert("更新失敗：" + error.message);
      }
    }
  </script>

  {{ live_script|safe }}
</body>
</html>
"""
