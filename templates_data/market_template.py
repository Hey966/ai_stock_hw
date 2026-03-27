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
      <a href="/stock">個股分析</a>
      <a href="/market">市場掃描</a>
      <a href="/daily">今日策略</a>
      <a href="/tools">進階分析工具</a>
    </div>

    <section class="market-hero">
      <div class="market-hero-badge">MARKET SCAN</div>
      <h1>📡 市場掃描儀表板</h1>
      <div class="subtitle">查看全市場分類結果、最新同步時間與掃描進度</div>
    </section>

    <section class="card market-summary-card">
      <h2 class="section-title"><span class="section-num">1</span>市場摘要</h2>

      <div class="market-status-row">
        <div class="market-status-chip">
          <div class="market-status-label">最近更新</div>
          <div class="market-status-value" id="market-updated-at">{{ market_sections["updated_at"] }}</div>
        </div>

        <div class="market-status-chip">
          <div class="market-status-label">掃描進度</div>
          <div class="market-status-value" id="market-progress">{{ market_sections["progress"]["processed"] }} / {{ market_sections["progress"]["total"] }}</div>
        </div>

        <div class="market-status-chip">
          <div class="market-status-label">最後更新股票</div>
          <div class="market-status-value" id="market-last-symbol">{{ market_sections["progress"]["last_symbol"] }}</div>
        </div>
      </div>

      <div class="market-bubble-grid">
        <div class="market-bubble market-bubble-blue">
          <div class="market-bubble-label">適合區</div>
          <div class="market-bubble-value" id="market-suitable-count">{{ market_sections["suitable"]|length }}</div>
        </div>

        <div class="market-bubble market-bubble-green">
          <div class="market-bubble-label">買入區</div>
          <div class="market-bubble-value" id="market-buy-count">{{ market_sections["buy"]|length }}</div>
        </div>

        <div class="market-bubble market-bubble-yellow">
          <div class="market-bubble-label">持有區</div>
          <div class="market-bubble-value" id="market-hold-count">{{ market_sections["hold"]|length }}</div>
        </div>

        <div class="market-bubble market-bubble-red">
          <div class="market-bubble-label">賣出區</div>
          <div class="market-bubble-value" id="market-sell-count">{{ market_sections["sell"]|length }}</div>
        </div>
      </div>
    </section>

    <section class="card market-section market-section-buy">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">2</span>買入區</h2>
        <div class="market-section-tag buy-tag">偏強勢 / 可優先關注</div>
      </div>

      <div class="stock-list" id="market-buy">
        {% for item in market_sections["buy"] %}
        <div class="stock-item stock-item-buy">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.company_name }}</div>
              <div class="stock-symbol">{{ item.symbol }}｜{{ item.suggestion }}</div>
            </div>
            <div class="stock-score stock-score-buy">分數 {{ item.score if item.score is defined else "N/A" }}</div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.latest_price if item.latest_price is defined else "N/A" }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.fair_value if item.fair_value is defined else "N/A" }}</div>
            </div>
          </div>
        </div>
        {% endfor %}

        {% if not market_sections["buy"] %}
        <div class="info-item">
          <div class="value">目前尚無買入區名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-hold">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">3</span>持有區</h2>
        <div class="market-section-tag hold-tag">中性區 / 持續觀察</div>
      </div>

      <div class="stock-list" id="market-hold">
        {% for item in market_sections["hold"] %}
        <div class="stock-item stock-item-hold">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.company_name }}</div>
              <div class="stock-symbol">{{ item.symbol }}｜{{ item.suggestion }}</div>
            </div>
            <div class="stock-score stock-score-hold">分數 {{ item.score if item.score is defined else "N/A" }}</div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.latest_price if item.latest_price is defined else "N/A" }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.fair_value if item.fair_value is defined else "N/A" }}</div>
            </div>
          </div>
        </div>
        {% endfor %}

        {% if not market_sections["hold"] %}
        <div class="info-item">
          <div class="value">目前尚無持有區名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-sell">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">4</span>賣出區</h2>
        <div class="market-section-tag sell-tag">偏弱勢 / 提高警覺</div>
      </div>

      <div class="stock-list" id="market-sell">
        {% for item in market_sections["sell"] %}
        <div class="stock-item stock-item-sell">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.company_name }}</div>
              <div class="stock-symbol">{{ item.symbol }}｜{{ item.suggestion }}</div>
            </div>
            <div class="stock-score stock-score-sell">分數 {{ item.score if item.score is defined else "N/A" }}</div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.latest_price if item.latest_price is defined else "N/A" }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.fair_value if item.fair_value is defined else "N/A" }}</div>
            </div>
          </div>
        </div>
        {% endfor %}

        {% if not market_sections["sell"] %}
        <div class="info-item">
          <div class="value">目前尚無賣出區名單。</div>
        </div>
        {% endif %}
      </div>
    </section>

    <section class="card market-section market-section-suitable">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">5</span>適合區</h2>
        <div class="market-section-tag suitable-tag">可追蹤 / 等待更佳時機</div>
      </div>

      <div class="stock-list" id="market-suitable">
        {% for item in market_sections["suitable"] %}
        <div class="stock-item stock-item-suitable">
          <div class="stock-head">
            <div>
              <div class="stock-name">{{ item.company_name }}</div>
              <div class="stock-symbol">{{ item.symbol }}｜{{ item.suggestion }}</div>
            </div>
            <div class="stock-score stock-score-suitable">分數 {{ item.score if item.score is defined else "N/A" }}</div>
          </div>

          <div class="stock-meta">
            <div class="stock-meta-box">
              <div class="stock-meta-label">最新價</div>
              <div class="stock-meta-value">{{ item.latest_price if item.latest_price is defined else "N/A" }}</div>
            </div>
            <div class="stock-meta-box">
              <div class="stock-meta-label">合理價</div>
              <div class="stock-meta-value">{{ item.fair_value if item.fair_value is defined else "N/A" }}</div>
            </div>
          </div>
        </div>
        {% endfor %}

        {% if not market_sections["suitable"] %}
        <div class="info-item">
          <div class="value">目前尚無適合區名單。</div>
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