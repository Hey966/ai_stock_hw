HOME_TEMPLATE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 投資分析平台</title>
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
      <div class="landing-badge">AI × 台股 × 新聞 × 價格歷程</div>
      <h1>打造你的智慧投資首頁</h1>
      <p class="landing-subtitle">
        這不是單純的股票查詢頁，而是一套整合基本面、價格結構、新聞事件、
        市場掃描與每日策略的 AI 投資分析平台。
      </p>

      <div class="landing-actions">
        <a class="cta-primary" href="/stock?symbol=2330">開始個股分析</a>
        <a class="cta-secondary" href="/market">查看市場掃描</a>
      </div>

      <div class="search-box" style="margin-top: 22px;">
        <form method="get" action="/stock">
          <div class="search-row">
            <input
              type="text"
              name="symbol"
              placeholder="輸入股票代號，例如 2330、2317、2454、0050"
              required
            >
            <button type="submit">查詢個股</button>
          </div>
        </form>
      </div>
    </section>

    <section class="feature-showcase">
      <div class="feature-card feature-card-a">
        <div class="feature-icon">📘</div>
        <div class="feature-title">個股分析</div>
        <div class="feature-text">
          查看單一股票的基本面、價格歷程、新聞分析與綜合評分。
        </div>
        <a href="/stock?symbol=2330">前往分析</a>
      </div>

      <div class="feature-card feature-card-b">
        <div class="feature-icon">📡</div>
        <div class="feature-title">市場掃描</div>
        <div class="feature-text">
          自動分類買入區、持有區、賣出區與觀察區，快速掌握全市場狀態。
        </div>
        <a href="/market">前往市場掃描</a>
      </div>

      <div class="feature-card feature-card-c">
        <div class="feature-icon">📅</div>
        <div class="feature-title">今日策略</div>
        <div class="feature-text">
          每日整理 Top Buy、今日觀察與風險名單，快速抓重點。
        </div>
        <a href="/daily">前往今日策略</a>
      </div>

      <div class="feature-card feature-card-d">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">進階工具</div>
        <div class="feature-text">
          進一步分析投資組合風險、產業結構與固定收益商品。
        </div>
        <a href="/tools">前往工具頁</a>
      </div>
    </section>

    <section class="card landing-status-card">
      <h2 class="section-title"><span class="section-num">1</span>系統狀態</h2>
      <div class="status-grid">
        <div class="status-pill">
          <div class="status-label">固定網址</div>
          <div class="status-value">
            <a href="https://app.ai966.online" target="_blank" rel="noopener noreferrer">
              app.ai966.online
            </a>
          </div>
        </div>

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

    <section class="card landing-summary-card">
      <h2 class="section-title"><span class="section-num">2</span>快速摘要</h2>
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

    <section class="card landing-guide-card">
      <h2 class="section-title"><span class="section-num">3</span>怎麼使用</h2>
      <div class="guide-steps">
        <div class="guide-step">
          <div class="guide-step-no">01</div>
          <div>
            <div class="guide-step-title">先看首頁摘要</div>
            <div class="guide-step-text">快速掌握市場區塊與今日策略數量變化。</div>
          </div>
        </div>

        <div class="guide-step">
          <div class="guide-step-no">02</div>
          <div>
            <div class="guide-step-title">輸入股票代號查詢</div>
            <div class="guide-step-text">可直接在首頁搜尋 2330、2317、2454、0050 等標的。</div>
          </div>
        </div>

        <div class="guide-step">
          <div class="guide-step-no">03</div>
          <div>
            <div class="guide-step-title">搭配市場掃描與今日策略</div>
            <div class="guide-step-text">建立整體市場視角，再回頭確認標的。</div>
          </div>
        </div>
      </div>
    </section>

    <div class="footer">AI Stock Dashboard</div>
  </div>
  {{ live_script|safe }}
</body>
</html>
"""