BASE_STYLE = """
<style>
  :root {
    --bg: #f3f6fb;
    --surface: #ffffff;
    --surface-soft: #f8fafc;
    --surface-muted: #eef3f8;
    --border: #dbe3ee;
    --text: #142033;
    --text-soft: #516074;
    --text-faint: #74839a;
    --primary: #2563eb;
    --primary-soft: #eaf2ff;
    --success: #15803d;
    --success-soft: #ecfdf3;
    --warning: #b45309;
    --warning-soft: #fff7ed;
    --danger: #b91c1c;
    --danger-soft: #fef2f2;
    --info: #1d4ed8;
    --info-soft: #eff6ff;
    --purple: #7c3aed;
    --purple-soft: #f5f3ff;
    --shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    --shadow-soft: 0 4px 12px rgba(15, 23, 42, 0.04);
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-sm: 10px;
  }

  * { box-sizing: border-box; }

  html, body {
    margin: 0;
    padding: 0;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", Arial, sans-serif;
    background: linear-gradient(180deg, #f8fafc 0%, var(--bg) 100%);
    color: var(--text);
    line-height: 1.6;
  }

  a {
    color: var(--primary);
  }

  .container {
    max-width: 1120px;
    margin: 0 auto;
    padding: 24px 16px 40px;
  }

  .nav {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 20px;
  }

  .nav a {
    text-decoration: none;
    color: var(--text);
    background: rgba(255,255,255,0.9);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 600;
    transition: all .18s ease;
    box-shadow: var(--shadow-soft);
  }

  .nav a:hover {
    background: #fff;
    border-color: #c9d5e4;
    transform: translateY(-1px);
  }

  .nav-home a:nth-child(1) {
    background: var(--primary-soft);
    color: var(--primary);
    border-color: #bfdbfe;
  }

  .hero, .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: var(--shadow);
  }

  .hero h1,
  .landing-hero h1,
  .market-hero h1,
  .daily-hero h1,
  .stock-hero h1,
  .tools-hero h1 {
    margin: 0;
    font-size: 34px;
    line-height: 1.2;
    color: var(--text);
    letter-spacing: -0.02em;
  }

  .subtitle,
  .landing-subtitle,
  .feature-text,
  .guide-step-text,
  .stock-reason,
  .value,
  .mode-card-text {
    color: var(--text-soft);
  }

  .subtitle {
    margin-top: 8px;
    font-size: 14px;
  }

  .search-box {
    margin-top: 18px;
    background: var(--surface-soft);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 14px;
  }

  .search-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  input, textarea, select, button {
    font: inherit;
    padding: 12px 14px;
    border-radius: 12px;
    border: 1px solid var(--border);
  }

  input, textarea, select {
    background: #fff;
    color: var(--text);
    width: 100%;
    outline: none;
  }

  input:focus, textarea:focus, select:focus {
    border-color: #93c5fd;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.08);
  }

  input { flex: 1; }

  textarea {
    min-height: 110px;
    resize: vertical;
  }

  button {
    background: var(--primary);
    color: #fff;
    border-color: var(--primary);
    cursor: pointer;
    font-weight: 600;
    transition: all .18s ease;
  }

  button:hover {
    filter: brightness(0.97);
    transform: translateY(-1px);
  }

  .cta-primary,
  .cta-secondary {
    text-decoration: none;
    padding: 12px 18px;
    border-radius: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid transparent;
  }

  .cta-primary {
    background: var(--primary);
    color: #fff;
  }

  .cta-secondary {
    background: #fff;
    color: var(--text);
    border-color: var(--border);
  }

  .landing-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 20px;
  }

  .landing-hero,
  .market-hero,
  .daily-hero,
  .stock-hero,
  .tools-hero {
    position: relative;
    overflow: hidden;
    padding: 28px 24px;
    margin-bottom: 18px;
    border-radius: 22px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    background:
      linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248,250,252,0.98));
  }

  .landing-badge,
  .market-hero-badge,
  .daily-badge,
  .stock-hero-badge,
  .tools-hero-badge {
    display: inline-block;
    margin-bottom: 14px;
    padding: 7px 12px;
    border-radius: 999px;
    background: var(--surface-muted);
    color: var(--text-faint);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .06em;
    border: 1px solid var(--border);
  }

  .landing-subtitle {
    margin-top: 14px;
    max-width: 760px;
    line-height: 1.8;
    font-size: 15px;
  }

  .feature-showcase,
  .mode-card-grid,
  .summary-grid,
  .landing-summary-grid,
  .stock-kpi-grid,
  .market-bubble-grid,
  .status-grid,
  .tools-form-grid,
  .metrics-grid {
    display: grid;
    gap: 14px;
  }

  .feature-showcase,
  .status-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }

  .summary-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }

  .landing-summary-grid,
  .stock-kpi-grid {
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  }

  .market-bubble-grid {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  }

  .tools-form-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }

  .metrics-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }

  .feature-card,
  .mode-card,
  .mini-card,
  .info-item,
  .stock-item,
  .stock-meta-box,
  .status-pill,
  .market-status-chip,
  .chart-box,
  .mode-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-soft);
  }

  .feature-card {
    padding: 18px;
    border-radius: 18px;
  }

  .feature-card a {
    color: var(--primary);
    font-weight: 600;
  }

  .feature-card-a,
  .feature-card-b,
  .feature-card-c,
  .feature-card-d,
  .risk-mode,
  .industry-mode,
  .fixed-mode {
    background: var(--surface);
  }

  .feature-icon,
  .mode-card-icon {
    font-size: 26px;
    margin-bottom: 10px;
  }

  .feature-title,
  .mode-card-title,
  .guide-step-title,
  .company-name,
  .stock-name,
  .section-title {
    color: var(--text);
  }

  .feature-title,
  .mode-card-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
  }

  .status-pill,
  .market-status-chip {
    border-radius: 16px;
    padding: 14px 16px;
  }

  .status-label,
  .market-status-label,
  .mini-title,
  .stock-meta-label,
  .summary-bubble-label,
  .stock-kpi-label,
  .market-bubble-label,
  .company-code,
  .hint,
  .footer {
    color: var(--text-faint);
  }

  .status-value,
  .market-status-value,
  .mini-value,
  .summary-bubble-value,
  .stock-kpi-value,
  .market-bubble-value,
  .stock-meta-value {
    color: var(--text);
    font-weight: 700;
  }

  .mini-card {
    border-radius: 16px;
    padding: 14px;
  }

  .mini-title {
    font-size: 13px;
    margin-bottom: 8px;
  }

  .mini-value {
    font-size: 22px;
  }

  .company-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 14px;
  }

  .company-name {
    font-size: 28px;
    font-weight: 800;
  }

  .tag,
  .market-section-tag {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    white-space: nowrap;
    border: 1px solid transparent;
  }

  .tag-buy, .buy-tag {
    background: var(--success-soft);
    color: var(--success);
    border-color: #bbf7d0;
  }

  .tag-hold, .hold-tag {
    background: var(--warning-soft);
    color: var(--warning);
    border-color: #fed7aa;
  }

  .tag-sell, .sell-tag {
    background: var(--danger-soft);
    color: var(--danger);
    border-color: #fecaca;
  }

  .tag-default,
  .suitable-tag {
    background: var(--info-soft);
    color: var(--info);
    border-color: #bfdbfe;
  }

  .section {
    margin-top: 12px;
  }

  .section-title {
    margin: 0 0 14px;
    font-size: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
  }

  .section-num {
    width: 30px;
    height: 30px;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid #bfdbfe;
  }

  .info-list,
  .stock-list,
  .guide-steps {
    display: grid;
    gap: 12px;
  }

  .info-item {
    border-radius: 14px;
    padding: 14px;
  }

  .label {
    color: var(--primary);
    font-weight: 700;
    margin-bottom: 6px;
    display: block;
  }

  .value {
    line-height: 1.75;
    word-break: break-word;
  }

  .stock-item {
    border-radius: 16px;
    padding: 14px;
  }

  .stock-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }

  .stock-name {
    font-size: 16px;
    font-weight: 700;
  }

  .stock-symbol {
    color: var(--text-faint);
    font-size: 13px;
    margin-top: 4px;
  }

  .stock-score {
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid var(--border);
    background: var(--surface-muted);
    color: var(--text-soft);
  }

  .stock-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
    margin-top: 10px;
  }

  .stock-meta-box {
    border-radius: 12px;
    padding: 10px;
    background: var(--surface-soft);
  }

  .stock-meta-label {
    font-size: 12px;
    margin-bottom: 6px;
  }

  .stock-meta-value {
    font-size: 14px;
  }

  .stock-reason {
    margin-top: 12px;
    line-height: 1.7;
  }

  .summary-bubble,
  .stock-kpi,
  .market-bubble {
    min-height: 118px;
    border-radius: 18px;
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    box-shadow: var(--shadow-soft);
    border: 1px solid var(--border);
    background: var(--surface);
  }

  .summary-bubble-label,
  .stock-kpi-label,
  .market-bubble-label {
    font-size: 13px;
    margin-bottom: 10px;
  }

  .summary-bubble-value,
  .stock-kpi-value,
  .market-bubble-value {
    font-size: 28px;
  }

  .bubble-green, .stock-kpi-green, .market-bubble-green {
    background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);
    border-color: #bbf7d0;
  }

  .bubble-yellow, .stock-kpi-yellow, .market-bubble-yellow {
    background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%);
    border-color: #fde68a;
  }

  .bubble-red, .stock-kpi-red, .market-bubble-red {
    background: linear-gradient(180deg, #fef2f2 0%, #ffffff 100%);
    border-color: #fecaca;
  }

  .bubble-blue, .stock-kpi-blue, .market-bubble-blue {
    background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%);
    border-color: #bfdbfe;
  }

  .bubble-purple, .stock-kpi-purple {
    background: linear-gradient(180deg, #f5f3ff 0%, #ffffff 100%);
    border-color: #ddd6fe;
  }

  .bubble-orange, .stock-kpi-orange {
    background: linear-gradient(180deg, #fff7ed 0%, #ffffff 100%);
    border-color: #fed7aa;
  }

  .bubble-pink, .stock-kpi-pink {
    background: linear-gradient(180deg, #fdf2f8 0%, #ffffff 100%);
    border-color: #fbcfe8;
  }

  .stock-kpi-indigo {
    background: linear-gradient(180deg, #eef2ff 0%, #ffffff 100%);
    border-color: #c7d2fe;
  }

  .guide-step {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 14px;
    box-shadow: var(--shadow-soft);
  }

  .guide-step-no {
    min-width: 46px;
    height: 46px;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    border: 1px solid #bfdbfe;
  }

  .market-summary-card,
  .stock-overview-card,
  .tools-form-card,
  .tools-result-card,
  .tools-empty-card,
  .market-section,
  .stock-section {
    border-radius: 18px;
  }

  .market-status-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
  }

  .market-section-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }

  .market-section-buy,
  .stock-section-b,
  .stock-section-f {
    border-top: 3px solid #22c55e;
  }

  .market-section-hold,
  .stock-section-e {
    border-top: 3px solid #f59e0b;
  }

  .market-section-sell,
  .stock-section-d {
    border-top: 3px solid #ef4444;
  }

  .market-section-suitable,
  .stock-section-a,
  .stock-section-g {
    border-top: 3px solid #3b82f6;
  }

  .stock-section-c {
    border-top: 3px solid #8b5cf6;
  }

  .stock-item-buy {
    background: #f8fff9;
    border-color: #d1fae5;
  }

  .stock-item-hold {
    background: #fffdfa;
    border-color: #fde68a;
  }

  .stock-item-sell {
    background: #fffafa;
    border-color: #fecaca;
  }

  .stock-item-suitable {
    background: #f8fbff;
    border-color: #bfdbfe;
  }

  .stock-score-buy {
    background: var(--success-soft);
    border-color: #bbf7d0;
    color: var(--success);
  }

  .stock-score-hold {
    background: var(--warning-soft);
    border-color: #fed7aa;
    color: var(--warning);
  }

  .stock-score-sell {
    background: var(--danger-soft);
    border-color: #fecaca;
    color: var(--danger);
  }

  .stock-score-suitable {
    background: var(--info-soft);
    border-color: #bfdbfe;
    color: var(--info);
  }

  .news-card {
    background: #fcfcff;
    border-color: #e9d5ff;
  }

  .chart-box {
    margin-top: 16px;
    border-radius: 16px;
    padding: 16px;
  }

  .chart-title {
    color: var(--text);
    font-weight: 700;
    margin-bottom: 12px;
  }

  .mode-card {
    text-align: left;
    border-radius: 16px;
    padding: 18px;
    color: var(--text);
    cursor: pointer;
    transition: all .18s ease;
  }

  .mode-card:hover,
  .mode-card-active {
    transform: translateY(-1px);
    border-color: #bfdbfe;
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.08);
  }

  .mode-panel {
    margin-top: 12px;
    padding: 16px;
    border-radius: 16px;
  }

  .footer {
    text-align: center;
    font-size: 12px;
    margin-top: 24px;
    padding-bottom: 30px;
  }

  @media (max-width: 640px) {
    .hero h1,
    .landing-hero h1,
    .market-hero h1,
    .daily-hero h1,
    .stock-hero h1,
    .tools-hero h1 {
      font-size: 28px;
    }

    .container {
      padding: 18px 12px 32px;
    }

    .company-name {
      font-size: 24px;
    }

    .mini-value,
    .summary-bubble-value,
    .stock-kpi-value,
    .market-bubble-value {
      font-size: 22px;
    }

    .section-title {
      font-size: 18px;
    }

    .summary-bubble,
    .market-bubble,
    .stock-kpi {
      min-height: 104px;
    }
  }
</style>
"""
