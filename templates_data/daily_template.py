DAILY_TEMPLATE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>今日策略</title>
  {{ base_style|safe }}
</head>
<body>
  <div class="container">
    <div class="nav">
      <a href="/">首頁</a>
      <a href="/stock">個股分析</a>
      <a href="/market">市場掃描</a>
      <a href="/daily">今日策略</a>
      <a href="/tools">進階分析工具</a>
    </div>

    <section class="daily-hero">
      <div class="daily-badge">DAILY STRATEGY</div>
      <h1>📅 今日策略儀表板</h1>
      <div class="subtitle">快速掌握今日市場重點與操作方向</div>
    </section>

    <section class="card">
      <h2 class="section-title"><span class="section-num">1</span>策略摘要</h2>

      <div class="market-status-row">
        <div class="market-status-chip">
          <div class="market-status-label">分析日期</div>
          <div class="market-status-value" id="daily-date">{{ daily_selection["date"] }}</div>
        </div>

        <div class="market-status-chip">
          <div class="market-status-label">更新時間</div>
          <div class="market-status-value" id="daily-updated-at">{{ daily_selection["updated_at"] }}</div>
        </div>
      </div>

      <div class="market-bubble-grid">
        <div class="market-bubble market-bubble-green">
          <div class="market-bubble-label">Top Buy</div>
          <div class="market-bubble-value" id="daily-top-count">{{ daily_selection["summary"]["top_buy_count"] }}</div>
        </div>

        <div class="market-bubble market-bubble-yellow">
          <div class="market-bubble-label">今日觀察</div>
          <div class="market-bubble-value" id="daily-watch-count">{{ daily_selection["summary"]["watch_hold_count"] }}</div>
        </div>

        <div class="market-bubble market-bubble-red">
          <div class="market-bubble-label">風險名單</div>
          <div class="market-bubble-value" id="daily-risk-count">{{ daily_selection["summary"]["risk_list_count"] }}</div>
        </div>
      </div>
    </section>

    <!-- Top Buy -->
    <section class="card market-section market-section-buy">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">2</span>Top Buy</h2>
        <div class="market-section-tag buy-tag">🔥 今日重點</div>
      </div>

      <div class="stock-list">
        {% for item in daily_selection["top_buy"] %}
        <div class="stock-item stock-item-buy">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.company_name }}</div>
              <div class="stock-symbol">{{ item.symbol }}｜{{ item.suggestion }}</div>
            </div>
            <div class="stock-score stock-score-buy">分數 {{ item.score }}</div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.latest_price }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.fair_value }}</div>
            </div>
          </div>

          <div class="stock-reason">{{ item.reason }}</div>
        </div>
        {% endfor %}
      </div>
    </section>

    <!-- Watch -->
    <section class="card market-section market-section-hold">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">3</span>今日觀察</h2>
        <div class="market-section-tag hold-tag">👀 觀察中</div>
      </div>

      <div class="stock-list">
        {% for item in daily_selection["watch_hold"] %}
        <div class="stock-item stock-item-hold">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.company_name }}</div>
              <div class="stock-symbol">{{ item.symbol }}｜{{ item.suggestion }}</div>
            </div>
            <div class="stock-score stock-score-hold">分數 {{ item.score }}</div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.latest_price }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.fair_value }}</div>
            </div>
          </div>

          <div class="stock-reason">{{ item.reason }}</div>
        </div>
        {% endfor %}
      </div>
    </section>

    <!-- Risk -->
    <section class="card market-section market-section-sell">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">4</span>風險名單</h2>
        <div class="market-section-tag sell-tag">⚠️ 注意風險</div>
      </div>

      <div class="stock-list">
        {% for item in daily_selection["risk_list"] %}
        <div class="stock-item stock-item-sell">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.company_name }}</div>
              <div class="stock-symbol">{{ item.symbol }}｜{{ item.suggestion }}</div>
            </div>
            <div class="stock-score stock-score-sell">分數 {{ item.score }}</div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.latest_price }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.fair_value }}</div>
            </div>
          </div>

          <div class="stock-reason">{{ item.reason }}</div>
        </div>
        {% endfor %}
      </div>
    </section>

    <div class="footer">AI Stock Dashboard</div>
  </div>
  {{ live_script|safe }}
</body>
</html>
"""