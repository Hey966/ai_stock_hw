TOOLS_TEMPLATE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>進階分析工具</title>
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

    <section class="tools-hero">
      <div class="tools-hero-badge">ADVANCED TOOLS</div>
      <h1>🧠 進階分析工具台</h1>
      <div class="subtitle">以卡片方式切換分析模式，操作更直覺</div>
    </section>

    <section class="card tools-form-card">
      <h2 class="section-title"><span class="section-num">1</span>選擇分析模式</h2>

      <form method="post" action="/tools" id="toolsForm">
        <input type="hidden" name="mode" id="modeInput" value="{{ mode }}">

        <div class="mode-card-grid">
          <button type="button" class="mode-card {% if mode == 'risk' %}mode-card-active risk-mode{% else %}risk-mode{% endif %}" onclick="selectMode('risk')">
            <div class="mode-card-icon">📉</div>
            <div class="mode-card-title">風險管理專家</div>
            <div class="mode-card-text">分析投資組合風險、VaR、CVaR、最大回檔與集中度。</div>
          </button>

          <button type="button" class="mode-card {% if mode == 'industry' %}mode-card-active industry-mode{% else %}industry-mode{% endif %}" onclick="selectMode('industry')">
            <div class="mode-card-icon">🏭</div>
            <div class="mode-card-title">產業分析師</div>
            <div class="mode-card-text">分析產業規模、成長動能、價值鏈、競爭格局與投資方向。</div>
          </button>

          <button type="button" class="mode-card {% if mode == 'fixed_income' %}mode-card-active fixed-mode{% else %}fixed-mode{% endif %}" onclick="selectMode('fixed_income')">
            <div class="mode-card-icon">💵</div>
            <div class="mode-card-title">固定收益分析專家</div>
            <div class="mode-card-text">計算殖利率、YTM、信用風險與固定收益商品比較。</div>
          </button>
        </div>

        <div id="riskFields" class="mode-panel" {% if mode != "risk" %}style="display:none;"{% endif %}>
          <div class="section">
            <label class="label">投資組合</label>
            <input type="text" name="positions" value="{{ positions_text }}" placeholder="格式：2330:40,2317:35,2603:25">
            <div class="hint">請輸入股票代號與權重，總和可不必剛好 100，系統會自動正規化。</div>
          </div>

          <div class="tools-form-grid">
            <div class="section">
              <label class="label">比較基準</label>
              <input type="text" name="benchmark" value="{{ benchmark }}" placeholder="例如：0050">
            </div>
            <div class="section">
              <label class="label">考量因素</label>
              <input type="text" name="factors" value="{{ factors }}" placeholder="例如：波動、景氣循環、流動性">
            </div>
          </div>
        </div>

        <div id="industryFields" class="mode-panel" {% if mode != "industry" %}style="display:none;"{% endif %}>
          <div class="tools-form-grid">
            <div class="section">
              <label class="label">產業名稱</label>
              <input type="text" name="target" value="{{ target }}" placeholder="例如：半導體 / 電子 / 航運">
            </div>
            <div class="section">
              <label class="label">比較基準</label>
              <input type="text" name="benchmark" value="{{ benchmark }}" placeholder="例如：台股 / 國際同業">
            </div>
          </div>

          <div class="section">
            <label class="label">考量因素</label>
            <textarea name="factors" placeholder="例如：景氣循環、技術門檻、資本支出">{{ factors }}</textarea>
          </div>
        </div>

        <div id="fixedFields" class="mode-panel" {% if mode != "fixed_income" %}style="display:none;"{% endif %}>
          <div class="tools-form-grid">
            <div class="section">
              <label class="label">商品名稱</label>
              <input type="text" name="target" value="{{ target }}" placeholder="例如：公司債A">
            </div>
            <div class="section">
              <label class="label">比較基準</label>
              <input type="text" name="benchmark" value="{{ benchmark }}" placeholder="例如：公債指數">
            </div>
          </div>

          <div class="section">
            <label class="label">考量因素</label>
            <textarea name="factors" placeholder="例如：信用風險、流動性、利率風險">{{ factors }}</textarea>
          </div>

          <div class="metrics-grid">
            <input type="text" name="price" value="{{ price }}" placeholder="價格，例如 98">
            <input type="text" name="face_value" value="{{ face_value }}" placeholder="面額，例如 100">
            <input type="text" name="coupon_rate" value="{{ coupon_rate }}" placeholder="票息，例如 0.03">
            <input type="text" name="years_to_maturity" value="{{ years_to_maturity }}" placeholder="到期年數，例如 5">
            <input type="text" name="credit_rating" value="{{ credit_rating }}" placeholder="信用評等，例如 A">
          </div>
        </div>

        <div class="section">
          <button type="submit">開始分析</button>
        </div>
      </form>
    </section>

    {% if mode == "risk" %}
      {% if risk_result %}
        <section class="card tools-result-card">
          <div class="market-section-head">
            <h2 class="section-title"><span class="section-num">2</span>量化指標</h2>
            <div class="market-section-tag hold-tag">風險儀表</div>
          </div>

          <div class="market-bubble-grid">
            <div class="market-bubble market-bubble-blue">
              <div class="market-bubble-label">VaR 95%</div>
              <div class="market-bubble-value">{{ risk_result.quant_metrics.VaR_95 }}</div>
            </div>
            <div class="market-bubble market-bubble-yellow">
              <div class="market-bubble-label">CVaR 95%</div>
              <div class="market-bubble-value">{{ risk_result.quant_metrics.CVaR_95 }}</div>
            </div>
            <div class="market-bubble market-bubble-red">
              <div class="market-bubble-label">最大回檔</div>
              <div class="market-bubble-value">{{ risk_result.quant_metrics.max_drawdown }}</div>
            </div>
          </div>
        </section>

        <section class="card tools-result-card">
          <div class="market-section-head">
            <h2 class="section-title"><span class="section-num">3</span>風險敞口分析</h2>
            <div class="market-section-tag suitable-tag">持股結構</div>
          </div>

          <div class="info-list">
            {% for p in risk_result.positions %}
            <div class="info-item">
              <span class="label">{{ p.name }} ({{ p.symbol }})</span>
              <div class="value">產業：{{ p.industry }}<br>權重：{{ p.weight }}%</div>
            </div>
            {% endfor %}
          </div>

          <div class="chart-box">
            <div class="chart-title">個股集中度長條圖</div>
            <canvas id="stockChart"></canvas>
          </div>
        </section>

        <section class="card tools-result-card">
          <div class="market-section-head">
            <h2 class="section-title"><span class="section-num">4</span>集中度分析</h2>
            <div class="market-section-tag buy-tag">產業配置</div>
          </div>

          <div class="info-list">
            {% for i in risk_result.industry_concentration %}
            <div class="info-item">
              <span class="label">{{ i.industry }}</span>
              <div class="value">產業權重：{{ i.weight }}%</div>
            </div>
            {% endfor %}
          </div>

          <div class="chart-box">
            <div class="chart-title">產業集中度圓餅圖</div>
            <canvas id="industryChart"></canvas>
          </div>
        </section>

        <section class="card tools-result-card">
          <div class="market-section-head">
            <h2 class="section-title"><span class="section-num">5</span>風險建議</h2>
            <div class="market-section-tag sell-tag">重點提醒</div>
          </div>

          <div class="info-item">
            <div class="value">
              <ul>
                {% for advice in risk_result.risk_advice %}
                <li>{{ advice }}</li>
                {% endfor %}
              </ul>
            </div>
          </div>
        </section>
      {% else %}
        <section class="card tools-empty-card">
          <h2 class="section-title"><span class="section-num">A</span>風險分析說明</h2>
          <div class="info-item">
            <div class="value">
              請先選擇「風險管理專家」，再輸入投資組合，例如：<br><br>
              2330:40,2317:35,2603:25
            </div>
          </div>
        </section>
      {% endif %}
    {% endif %}

    {% if mode == "industry" %}
      {% if industry_result %}
        <section class="card tools-result-card">
          <h2 class="section-title"><span class="section-num">2</span>產業概覽</h2>
          <div class="info-item">
            <div class="value">{{ industry_result.industry_overview.market_size_and_growth }}</div>
          </div>
        </section>

        <section class="card tools-result-card">
          <h2 class="section-title"><span class="section-num">3</span>價值鏈分析</h2>
          <div class="info-item">
            <div class="value">{{ industry_result.value_chain }}</div>
          </div>
        </section>

        <section class="card tools-result-card">
          <h2 class="section-title"><span class="section-num">4</span>競爭格局</h2>
          <div class="info-item">
            <div class="value">{{ industry_result.competition }}</div>
          </div>
        </section>

        <section class="card tools-result-card">
          <h2 class="section-title"><span class="section-num">5</span>成長驅動因素與挑戰</h2>
          <div class="info-list">
            <div class="info-item">
              <span class="label">成長驅動因素</span>
              <div class="value">{{ industry_result.drivers_and_challenges.drivers }}</div>
            </div>
            <div class="info-item">
              <span class="label">挑戰</span>
              <div class="value">{{ industry_result.drivers_and_challenges.challenges }}</div>
            </div>
          </div>
        </section>

        <section class="card tools-result-card">
          <h2 class="section-title"><span class="section-num">6</span>投資建議</h2>
          <div class="info-item">
            <div class="value">{{ industry_result.investment_ideas }}</div>
          </div>
        </section>
      {% else %}
        <section class="card tools-empty-card">
          <h2 class="section-title"><span class="section-num">A</span>產業分析說明</h2>
          <div class="info-item">
            <div class="value">
              請先選擇「產業分析師」，再輸入產業名稱，例如：<br><br>
              半導體 / 電子 / 航運
            </div>
          </div>
        </section>
      {% endif %}
    {% endif %}

    {% if mode == "fixed_income" %}
      {% if fixed_income_result %}
        <section class="card tools-result-card">
          <div class="market-section-head">
            <h2 class="section-title"><span class="section-num">2</span>殖利率計算</h2>
            <div class="market-section-tag buy-tag">固定收益</div>
          </div>

          <div class="market-bubble-grid">
            <div class="market-bubble market-bubble-blue">
              <div class="market-bubble-label">名目殖利率</div>
              <div class="market-bubble-value">{{ fixed_income_result.nominal_yield }}</div>
            </div>
            <div class="market-bubble market-bubble-green">
              <div class="market-bubble-label">YTM</div>
              <div class="market-bubble-value">{{ fixed_income_result.ytm }}</div>
            </div>
            <div class="market-bubble market-bubble-purple">
              <div class="market-bubble-label">信用評等</div>
              <div class="market-bubble-value">{{ fixed_income_result.credit_rating }}</div>
            </div>
          </div>
        </section>

        <section class="card tools-result-card">
          <h2 class="section-title"><span class="section-num">3</span>風險與比較</h2>
          <div class="info-list">
            <div class="info-item">
              <span class="label">信用風險</span>
              <div class="value">{{ fixed_income_result.credit_risk_note }}</div>
            </div>
            <div class="info-item">
              <span class="label">同業比較</span>
              <div class="value">{{ fixed_income_result.peer_comparison_note }}</div>
            </div>
            <div class="info-item">
              <span class="label">投資建議</span>
              <div class="value">{{ fixed_income_result.investment_advice }}</div>
            </div>
          </div>
        </section>
      {% else %}
        <section class="card tools-empty-card">
          <h2 class="section-title"><span class="section-num">A</span>固定收益分析說明</h2>
          <div class="info-item">
            <div class="value">
              請先選擇「固定收益分析專家」，再輸入商品與參數，例如：<br><br>
              標的：公司債A<br>
              價格：98<br>
              面額：100<br>
              票息：0.03<br>
              到期年數：5<br>
              信用評等：A
            </div>
          </div>
        </section>
      {% endif %}
    {% endif %}
  </div>

  {% if risk_result %}
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    const stockLabels = {{ stock_labels | tojson }};
    const stockWeights = {{ stock_weights | tojson }};
    const industryLabels = {{ industry_labels | tojson }};
    const industryWeights = {{ industry_weights | tojson }};

    const stockCtx = document.getElementById('stockChart');
    if (stockCtx) {
      new Chart(stockCtx, {
        type: 'bar',
        data: {
          labels: stockLabels,
          datasets: [{
            label: '個股權重 (%)',
            data: stockWeights,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: { color: 'white' }
            }
          },
          scales: {
            x: {
              ticks: { color: '#cbd5e1' },
              grid: { color: 'rgba(255,255,255,0.06)' }
            },
            y: {
              beginAtZero: true,
              ticks: { color: '#cbd5e1' },
              grid: { color: 'rgba(255,255,255,0.06)' }
            }
          }
        }
      });
    }

    const industryCtx = document.getElementById('industryChart');
    if (industryCtx) {
      new Chart(industryCtx, {
        type: 'pie',
        data: {
          labels: industryLabels,
          datasets: [{
            data: industryWeights
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: { color: 'white' }
            }
          }
        }
      });
    }

    function selectMode(mode) {
      document.getElementById("modeInput").value = mode;

      document.querySelectorAll(".mode-card").forEach(card => {
        card.classList.remove("mode-card-active");
      });

      document.getElementById("riskFields").style.display = "none";
      document.getElementById("industryFields").style.display = "none";
      document.getElementById("fixedFields").style.display = "none";

      if (mode === "risk") {
        document.querySelector(".risk-mode").classList.add("mode-card-active");
        document.getElementById("riskFields").style.display = "block";
      } else if (mode === "industry") {
        document.querySelector(".industry-mode").classList.add("mode-card-active");
        document.getElementById("industryFields").style.display = "block";
      } else if (mode === "fixed_income") {
        document.querySelector(".fixed-mode").classList.add("mode-card-active");
        document.getElementById("fixedFields").style.display = "block";
      }
    }
  </script>
  {% else %}
  <script>
    function selectMode(mode) {
      document.getElementById("modeInput").value = mode;

      document.querySelectorAll(".mode-card").forEach(card => {
        card.classList.remove("mode-card-active");
      });

      document.getElementById("riskFields").style.display = "none";
      document.getElementById("industryFields").style.display = "none";
      document.getElementById("fixedFields").style.display = "none";

      if (mode === "risk") {
        document.querySelector(".risk-mode").classList.add("mode-card-active");
        document.getElementById("riskFields").style.display = "block";
      } else if (mode === "industry") {
        document.querySelector(".industry-mode").classList.add("mode-card-active");
        document.getElementById("industryFields").style.display = "block";
      } else if (mode === "fixed_income") {
        document.querySelector(".fixed-mode").classList.add("mode-card-active");
        document.getElementById("fixedFields").style.display = "block";
      }
    }
  </script>
  {% endif %}
</body>
</html>
"""