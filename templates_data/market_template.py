MARKET_TEMPLATE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>市場掃描</title>
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

    <section class="market-hero">
      <div class="market-hero-badge">市場掃描</div>
      <h1>用分類方式掌握目前市場狀態</h1>
      <div class="subtitle">從買入、持有、賣出與觀察區塊快速瀏覽全市場結果，先看全貌，再決定下一步。</div>
    </section>

    <section class="card market-summary-card">
      <h2 class="section-title"><span class="section-num">1</span>市場摘要</h2>

      <div class="market-status-row">
        <div class="market-status-chip">
          <div class="market-status-label">最近更新</div>
          <div class="market-status-value" id="market-updated-at">
            {{ market_sections.get("updated_at", "N/A") }}
          </div>
        </div>

        <div class="market-status-chip">
          <div class="market-status-label">掃描總數</div>
          <div class="market-status-value" id="market-total-scanned">
            {{ market_sections.get("total_scanned", 0) }}
          </div>
        </div>

        <div class="market-status-chip">
          <div class="market-status-label">錯誤數量</div>
          <div class="market-status-value" id="market-error-count">
            {{ market_sections.get("error_count", 0) }}
          </div>
        </div>
      </div>

      <div class="market-bubble-grid">
        <div class="market-bubble market-bubble-green">
          <div class="market-bubble-label">買入區</div>
          <div class="market-bubble-value" id="market-buy-count">
            {{ market_sections.get("buy_count", market_sections.get("buy", [])|length) }}
          </div>
        </div>

        <div class="market-bubble market-bubble-yellow">
          <div class="market-bubble-label">持有區</div>
          <div class="market-bubble-value" id="market-hold-count">
            {{ market_sections.get("hold_count", market_sections.get("hold", [])|length) }}
          </div>
        </div>

        <div class="market-bubble market-bubble-red">
          <div class="market-bubble-label">賣出區</div>
          <div class="market-bubble-value" id="market-sell-count">
            {{ market_sections.get("sell_count", market_sections.get("sell", [])|length) }}
          </div>
        </div>

        <div class="market-bubble market-bubble-blue">
          <div class="market-bubble-label">觀察區</div>
          <div class="market-bubble-value" id="market-watch-count">
            {{ market_sections.get("watch_count", market_sections.get("watch", [])|length) }}
          </div>
        </div>
      </div>
    </section>

    <section class="card market-section market-section-buy">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">2</span>買入區</h2>
        <div class="market-section-tag buy-tag">優先關注</div>
      </div>

      <div class="stock-list" id="market-buy">
        {% for item in market_sections.get("buy", []) %}
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

        {% if not market_sections.get("buy", []) %}
        <div class="info-item">
          <div class="value">目前尚無買入區名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-hold">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">3</span>持有區</h2>
        <div class="market-section-tag hold-tag">持續觀察</div>
      </div>

      <div class="stock-list" id="market-hold">
        {% for item in market_sections.get("hold", []) %}
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

        {% if not market_sections.get("hold", []) %}
        <div class="info-item">
          <div class="value">目前尚無持有區名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-sell">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">4</span>賣出區</h2>
        <div class="market-section-tag sell-tag">提高警覺</div>
      </div>

      <div class="stock-list" id="market-sell">
        {% for item in market_sections.get("sell", []) %}
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

        {% if not market_sections.get("sell", []) %}
        <div class="info-item">
          <div class="value">目前尚無賣出區名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-suitable">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">5</span>觀察區</h2>
        <div class="market-section-tag suitable-tag">等待更佳時機</div>
      </div>

      <div class="stock-list" id="market-watch">
        {% for item in market_sections.get("watch", []) %}
        <div class="stock-item stock-item-suitable">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.get("company_name", "-") }}</div>
              <div class="stock-symbol">{{ item.get("symbol", "-") }}｜{{ item.get("signal", "-") }}</div>
            </div>
            <div class="stock-score stock-score-suitable">
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

        {% if not market_sections.get("watch", []) %}
        <div class="info-item">
          <div class="value">目前尚無觀察區名單。</div>
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
