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
      <a href="/stock?symbol=2330">個股分析</a>
      <a href="/market">市場掃描</a>
      <a href="/daily">今日策略</a>
      <a href="/tools">進階分析工具</a>
    </div>

    <section class="daily-hero">
      <div class="daily-badge">今日策略</div>
      <h1>把每日重點整理成可直接瀏覽的名單</h1>
      <div class="subtitle">集中查看 Top Buy、觀察名單與風險名單，快速掌握今天最值得留意的方向。</div>
    </section>

    <section class="card">
      <h2 class="section-title"><span class="section-num">1</span>策略摘要</h2>

      <div class="market-status-row">
        <div class="market-status-chip">
          <div class="market-status-label">分析日期</div>
          <div class="market-status-value" id="daily-date">
            {{ daily_selection.get("date", "尚未產生") }}
          </div>
        </div>

        <div class="market-status-chip">
          <div class="market-status-label">更新時間</div>
          <div class="market-status-value" id="daily-updated-at">
            {{ daily_selection.get("updated_at", "尚未產生") }}
          </div>
        </div>
      </div>

      <div class="market-bubble-grid">
        <div class="market-bubble market-bubble-green">
          <div class="market-bubble-label">Top Buy</div>
          <div class="market-bubble-value" id="daily-top-count">
            {{ daily_selection.get("summary", {}).get("top_buy_count", 0) }}
          </div>
        </div>

        <div class="market-bubble market-bubble-yellow">
          <div class="market-bubble-label">今日觀察</div>
          <div class="market-bubble-value" id="daily-watch-count">
            {{ daily_selection.get("summary", {}).get("watch_hold_count", 0) }}
          </div>
        </div>

        <div class="market-bubble market-bubble-red">
          <div class="market-bubble-label">風險名單</div>
          <div class="market-bubble-value" id="daily-risk-count">
            {{ daily_selection.get("summary", {}).get("risk_list_count", 0) }}
          </div>
        </div>
      </div>
    </section>

    <section class="card market-section market-section-buy">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">2</span>Top Buy</h2>
        <div class="market-section-tag buy-tag">今日優先關注</div>
      </div>

      <div class="stock-list">
        {% for item in daily_selection.get("top_buy", []) %}
        <div class="stock-item stock-item-buy">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.get("company_name", "-") }}</div>
              <div class="stock-symbol">{{ item.get("symbol", "-") }}｜{{ item.get("signal", "-") }}</div>
            </div>
            <div class="stock-score stock-score-buy">
              漲跌 {{ item.get("daily_change_pct", "N/A") }}%
            </div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.get("price", "N/A") }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">MA20</div>
              <div class="stock-meta-value">{{ item.get("ma20", "N/A") }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.get("fair_value", "N/A") }}</div>
            </div>
          </div>

          <div class="stock-reason">{{ item.get("reason", "無分析原因") }}</div>
        </div>
        {% endfor %}

        {% if not daily_selection.get("top_buy", []) %}
        <div class="info-item">
          <div class="value">目前尚無 Top Buy 名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-hold">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">3</span>今日觀察</h2>
        <div class="market-section-tag hold-tag">持續追蹤</div>
      </div>

      <div class="stock-list">
        {% for item in daily_selection.get("watch_hold", []) %}
        <div class="stock-item stock-item-hold">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.get("company_name", "-") }}</div>
              <div class="stock-symbol">{{ item.get("symbol", "-") }}｜{{ item.get("signal", "-") }}</div>
            </div>
            <div class="stock-score stock-score-hold">
              漲跌 {{ item.get("daily_change_pct", "N/A") }}%
            </div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.get("price", "N/A") }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">MA20</div>
              <div class="stock-meta-value">{{ item.get("ma20", "N/A") }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.get("fair_value", "N/A") }}</div>
            </div>
          </div>

          <div class="stock-reason">{{ item.get("reason", "無分析原因") }}</div>
        </div>
        {% endfor %}

        {% if not daily_selection.get("watch_hold", []) %}
        <div class="info-item">
          <div class="value">目前尚無今日觀察名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-sell">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">4</span>風險名單</h2>
        <div class="market-section-tag sell-tag">注意風險</div>
      </div>

      <div class="stock-list">
        {% for item in daily_selection.get("risk_list", []) %}
        <div class="stock-item stock-item-sell">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.get("company_name", "-") }}</div>
              <div class="stock-symbol">{{ item.get("symbol", "-") }}｜{{ item.get("signal", "-") }}</div>
            </div>
            <div class="stock-score stock-score-sell">
              漲跌 {{ item.get("daily_change_pct", "N/A") }}%
            </div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.get("price", "N/A") }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">MA20</div>
              <div class="stock-meta-value">{{ item.get("ma20", "N/A") }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.get("fair_value", "N/A") }}</div>
            </div>
          </div>

          <div class="stock-reason">{{ item.get("reason", "無分析原因") }}</div>
        </div>
        {% endfor %}

        {% if not daily_selection.get("risk_list", []) %}
        <div class="info-item">
          <div class="value">目前尚無風險名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <div class="footer">AI Stock Dashboard</div>
  </div>
  {{ live_script|safe }}
</body>
</html>
"""
