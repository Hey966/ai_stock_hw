STOCK_TEMPLATE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>個股詳細分析</title>
  {{ base_style|safe }}
</head>
<body>
  <div class="container">
    <div class="nav">
      <a href="/">首頁</a>
      <a href="/stock?symbol={{ symbol }}">個股分析</a>
      <a href="/market">市場掃描</a>
      <a href="/daily">今日策略</a>
      <a href="/tools">進階分析工具</a>
    </div>

    <section class="stock-hero">
      <div class="stock-hero-badge">STOCK ANALYSIS</div>
      <h1>📘 個股詳細分析</h1>
      <div class="subtitle">基本面、估值、價格歷程與新聞分析整合</div>

      <div class="search-box">
        <form method="get" action="/stock">
          <div class="search-row">
            <input type="text" name="symbol" value="{{ symbol }}" placeholder="輸入台股代號，例如 2330">
            <button type="submit">查詢個股</button>
          </div>
        </form>
      </div>
    </section>

    <section class="card stock-overview-card">
      <div class="company-row">
        <div>
          <div class="company-name">{{ report.company_name }}</div>
          <div class="company-code">股票代號：{{ report.symbol }}</div>
        </div>
        <div class="tag {{ suggestion_css }}">{{ valuation.investment_suggestion }}</div>
      </div>

      <div class="stock-kpi-grid">
        <div class="stock-kpi stock-kpi-blue">
          <div class="stock-kpi-label">最新股價</div>
          <div class="stock-kpi-value">{{ report.latest_price }}</div>
        </div>
        <div class="stock-kpi stock-kpi-indigo">
          <div class="stock-kpi-label">價格日期</div>
          <div class="stock-kpi-value">{{ report.latest_price_date }}</div>
        </div>
        <div class="stock-kpi stock-kpi-purple">
          <div class="stock-kpi-label">綜合評分</div>
          <div class="stock-kpi-value">{{ valuation.score }}</div>
        </div>
        <div class="stock-kpi stock-kpi-green">
          <div class="stock-kpi-label">投資建議</div>
          <div class="stock-kpi-value">{{ valuation.investment_suggestion }}</div>
        </div>
        <div class="stock-kpi stock-kpi-pink">
          <div class="stock-kpi-label">新聞分數</div>
          <div class="stock-kpi-value">{{ valuation.news_score }}</div>
        </div>
      </div>
    </section>

    <section class="card stock-section stock-section-a">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">1</span>企業概覽</h2>
        <div class="market-section-tag suitable-tag">公司定位</div>
      </div>

      <div class="info-list">
        <div class="info-item">
          <span class="label">產業類別</span>
          <div class="value">{{ report.enterprise_overview.industry_category }}</div>
        </div>
        <div class="info-item">
          <span class="label">主要產品 / 服務</span>
          <div class="value">{{ report.enterprise_overview.main_products_services }}</div>
        </div>
        <div class="info-item">
          <span class="label">市場地位</span>
          <div class="value">{{ report.enterprise_overview.market_position }}</div>
        </div>
      </div>
    </section>

    <section class="card stock-section stock-section-b">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">2</span>財務表現</h2>
        <div class="market-section-tag buy-tag">基本面</div>
      </div>

      <div class="summary-grid">
        <div class="mini-card">
          <div class="mini-title">毛利率</div>
          <div class="mini-value">{{ report.financial_performance.gross_margin }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">ROE</div>
          <div class="mini-value">{{ report.financial_performance.roe }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">負債比</div>
          <div class="mini-value">{{ report.financial_performance.debt_ratio }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">Debt / Equity</div>
          <div class="mini-value">{{ report.financial_performance.debt_to_equity }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">PBR</div>
          <div class="mini-value">{{ report.financial_performance.pbr }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">本益比</div>
          <div class="mini-value">{{ report.financial_performance.trailing_pe }}</div>
        </div>
      </div>

      <div class="section">
        <div class="mini-title">近三年營收趨勢</div>
        <div class="info-list">
          {% for item in report.financial_performance.revenue_trend_3y %}
          <div class="info-item">
            <span class="label">{{ item.year }}</span>
            <div class="value">{{ item.revenue }}</div>
          </div>
          {% endfor %}
        </div>
      </div>
    </section>

    <section class="card stock-section stock-section-c">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">3</span>競爭優勢</h2>
        <div class="market-section-tag hold-tag">護城河</div>
      </div>
      <div class="info-item">
        <div class="value">{{ report.competitive_advantage }}</div>
      </div>
    </section>

    <section class="card stock-section stock-section-d">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">4</span>風險評估</h2>
        <div class="market-section-tag sell-tag">風險提醒</div>
      </div>
      <div class="info-item">
        <div class="value">{{ report.risk_assessment }}</div>
      </div>
    </section>

    <section class="card stock-section stock-section-e">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">5</span>價格歷程分析</h2>
        <div class="market-section-tag suitable-tag">技術面</div>
      </div>

      <div class="stock-kpi-grid">
        <div class="stock-kpi stock-kpi-blue">
          <div class="stock-kpi-label">趨勢</div>
          <div class="stock-kpi-value">{{ report.price_analysis.trend }}</div>
        </div>
        <div class="stock-kpi stock-kpi-orange">
          <div class="stock-kpi-label">波動度</div>
          <div class="stock-kpi-value">{{ report.price_analysis.volatility }}</div>
        </div>
        <div class="stock-kpi stock-kpi-purple">
          <div class="stock-kpi-label">動能</div>
          <div class="stock-kpi-value">{{ report.price_analysis.momentum }}</div>
        </div>
        <div class="stock-kpi stock-kpi-green">
          <div class="stock-kpi-label">價格分析分數</div>
          <div class="stock-kpi-value">{{ report.price_analysis.score }}</div>
        </div>
      </div>
    </section>

    <section class="card stock-section stock-section-f">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">6</span>估值判斷</h2>
        <div class="market-section-tag buy-tag">估值結論</div>
      </div>

      <div class="info-list">
        <div class="info-item">
          <span class="label">本益比區間</span>
          <div class="value">{{ valuation.pe_range }}</div>
        </div>
        <div class="info-item">
          <span class="label">理由</span>
          <div class="value">{{ valuation.reason }}</div>
        </div>
        <div class="info-item">
          <span class="label">合理價</span>
          <div class="value">{{ valuation.fair_value }}</div>
        </div>
        <div class="info-item">
          <span class="label">MA20</span>
          <div class="value">{{ valuation.ma20 }}</div>
        </div>
      </div>

      <div class="summary-grid">
        <div class="mini-card">
          <div class="mini-title">價值分數</div>
          <div class="mini-value">{{ valuation.valuation_score }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">品質分數</div>
          <div class="mini-value">{{ valuation.quality_score }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">成長分數</div>
          <div class="mini-value">{{ valuation.growth_score }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">技術分數</div>
          <div class="mini-value">{{ valuation.technical_score }}</div>
        </div>
        <div class="mini-card">
          <div class="mini-title">新聞分數</div>
          <div class="mini-value">{{ valuation.news_score }}</div>
        </div>
      </div>
    </section>

    <section class="card stock-section stock-section-g">
      <div class="market-section-head">
        <h2 class="section-title"><span class="section-num">7</span>新聞分析</h2>
        <div class="market-section-tag hold-tag">事件與情緒</div>
      </div>

      <div class="stock-kpi-grid">
        <div class="stock-kpi stock-kpi-blue">
          <div class="stock-kpi-label">新聞數量</div>
          <div class="stock-kpi-value">{{ report.news_analysis.headline_count }}</div>
        </div>
        <div class="stock-kpi stock-kpi-green">
          <div class="stock-kpi-label">偏多新聞</div>
          <div class="stock-kpi-value">{{ report.news_analysis.positive_count }}</div>
        </div>
        <div class="stock-kpi stock-kpi-red">
          <div class="stock-kpi-label">偏空新聞</div>
          <div class="stock-kpi-value">{{ report.news_analysis.negative_count }}</div>
        </div>
        <div class="stock-kpi stock-kpi-purple">
          <div class="stock-kpi-label">情緒分數</div>
          <div class="stock-kpi-value">{{ report.news_analysis.sentiment_score }}</div>
        </div>
        <div class="stock-kpi stock-kpi-orange">
          <div class="stock-kpi-label">事件風險</div>
          <div class="stock-kpi-value">{{ report.news_analysis.risk_level }}</div>
        </div>
      </div>

      <div class="section">
        <div class="mini-title">新聞摘要</div>
        <div class="info-item">
          <div class="value">{{ report.news_analysis.summary }}</div>
        </div>
      </div>

      <div class="section">
        <div class="mini-title">最近新聞</div>
        <div class="info-list">
          {% if report.news_analysis.top_news %}
            {% for item in report.news_analysis.top_news %}
            <div class="info-item news-card">
              <span class="label">{{ item.source }}</span>
              <div class="value">
                <div style="font-weight:600; margin-bottom:6px;">{{ item.title }}</div>
                <div style="font-size:13px; opacity:.8; margin-bottom:6px;">{{ item.published_at }}</div>
                {% if item.url %}
                <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer">查看新聞</a>
                {% endif %}
              </div>
            </div>
            {% endfor %}
          {% else %}
            <div class="info-item">
              <div class="value">目前沒有可顯示的新聞資料。</div>
            </div>
          {% endif %}
        </div>
      </div>
    </section>

    <div class="footer">AI Stock Dashboard</div>
  </div>
  {{ live_script|safe }}
</body>
</html>
"""