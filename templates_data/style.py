BASE_STYLE = """
<style>
  * { box-sizing: border-box; }

  body {
    margin: 0;
    font-family: Arial, sans-serif;
    background:
      radial-gradient(circle at top left, rgba(59,130,246,0.16), transparent 28%),
      radial-gradient(circle at top right, rgba(236,72,153,0.12), transparent 24%),
      radial-gradient(circle at bottom left, rgba(34,197,94,0.10), transparent 26%),
      linear-gradient(145deg, #07101d 0%, #0b1220 40%, #111827 100%);
    color: #e5eefc;
  }

  .container {
    max-width: 1080px;
    margin: 0 auto;
    padding: 18px 14px 44px;
  }

  .nav {
    display: flex;
    gap: 12px;
    margin-bottom: 18px;
    flex-wrap: wrap;
  }

  .nav a {
    color: #dbeafe;
    text-decoration: none;
    background: rgba(15,23,42,0.72);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 999px;
    padding: 10px 16px;
    transition: all .2s ease;
  }

  .nav a:hover {
    transform: translateY(-1px);
    background: rgba(30,41,59,0.92);
  }

  .nav-home a:nth-child(1) { background: rgba(59,130,246,0.22); }
  .nav-home a:nth-child(2) { background: rgba(34,197,94,0.18); }
  .nav-home a:nth-child(3) { background: rgba(245,158,11,0.18); }
  .nav-home a:nth-child(4) { background: rgba(168,85,247,0.18); }
  .nav-home a:nth-child(5) { background: rgba(236,72,153,0.16); }

  .hero, .card {
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 24px;
    padding: 18px;
    margin-bottom: 16px;
    backdrop-filter: blur(8px);
  }

  .hero h1 {
    margin: 0;
    font-size: 30px;
    color: #ffffff;
  }

  .subtitle {
    margin-top: 8px;
    color: #b8c7dd;
    font-size: 14px;
  }

  .search-box {
    margin-top: 18px;
    background: rgba(7,16,29,0.60);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 20px;
    padding: 14px;
  }

  .search-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  input, textarea, select, button {
    padding: 12px 14px;
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,0.15);
    font-size: 16px;
  }

  input, textarea, select {
    background: #0f172a;
    color: white;
    width: 100%;
  }

  input { flex: 1; }

  textarea {
    min-height: 100px;
    resize: vertical;
  }

  button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    cursor: pointer;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
  }

  .mini-card {
    background: linear-gradient(180deg, rgba(17,24,39,0.92), rgba(11,18,32,0.72));
    border-radius: 22px;
    padding: 14px;
    border: 1px solid rgba(148,163,184,0.08);
  }

  .mini-title {
    font-size: 13px;
    color: #9fb0c7;
    margin-bottom: 8px;
  }

  .mini-value {
    font-size: 22px;
    font-weight: bold;
    color: white;
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
    font-weight: bold;
    color: #ffffff;
  }

  .company-code, .hint, .footer {
    color: #9fb0c7;
  }

  .tag {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: bold;
    white-space: nowrap;
  }

  .tag-buy {
    background: rgba(34,197,94,0.18);
    color: #86efac;
    border: 1px solid rgba(34,197,94,0.28);
  }

  .tag-hold {
    background: rgba(245,158,11,0.18);
    color: #fcd34d;
    border: 1px solid rgba(245,158,11,0.28);
  }

  .tag-sell {
    background: rgba(239,68,68,0.18);
    color: #fca5a5;
    border: 1px solid rgba(239,68,68,0.28);
  }

  .tag-default {
    background: rgba(148,163,184,0.16);
    color: #cbd5e1;
    border: 1px solid rgba(148,163,184,0.22);
  }

  .section {
    margin-top: 12px;
  }

  .section-title {
    margin: 0 0 14px;
    font-size: 20px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .section-num {
    width: 32px;
    height: 32px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(37,99,235,0.25), rgba(168,85,247,0.22));
    color: #dbeafe;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: bold;
    border: 1px solid rgba(125,211,252,0.20);
  }

  .info-list {
    display: grid;
    gap: 12px;
  }

  .info-item {
    background: rgba(11,18,32,0.72);
    border-radius: 20px;
    padding: 14px;
    border: 1px solid rgba(148,163,184,0.08);
  }

  .label {
    color: #8fb4ff;
    font-weight: bold;
    margin-bottom: 6px;
    display: block;
  }

  .value {
    color: #e5eefc;
    line-height: 1.7;
    word-break: break-word;
  }

  .stock-list {
    display: grid;
    gap: 12px;
    margin-top: 14px;
  }

  .stock-item {
    background: linear-gradient(180deg, rgba(15,23,42,0.86), rgba(11,18,32,0.72));
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 22px;
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
    font-weight: bold;
    color: #ffffff;
  }

  .stock-symbol {
    color: #8fb4ff;
    font-size: 13px;
    margin-top: 4px;
  }

  .stock-score {
    background: linear-gradient(135deg, rgba(37,99,235,0.20), rgba(168,85,247,0.18));
    border: 1px solid rgba(37,99,235,0.28);
    color: #c4b5fd;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: bold;
  }

  .stock-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
    margin-top: 10px;
  }

  .stock-meta-box {
    background: rgba(15,23,42,0.7);
    border-radius: 18px;
    padding: 10px;
    border: 1px solid rgba(148,163,184,0.06);
  }

  .stock-meta-label {
    color: #9fb0c7;
    font-size: 12px;
    margin-bottom: 6px;
  }

  .stock-meta-value {
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
  }

  .stock-reason {
    margin-top: 12px;
    line-height: 1.7;
    color: #dbe7f7;
  }

  .landing-hero {
    position: relative;
    overflow: hidden;
    padding: 30px 24px;
    margin-bottom: 18px;
    border-radius: 34px 18px 34px 18px;
    background:
      radial-gradient(circle at 20% 20%, rgba(96,165,250,0.28), transparent 28%),
      radial-gradient(circle at 80% 25%, rgba(236,72,153,0.20), transparent 24%),
      radial-gradient(circle at 50% 100%, rgba(34,197,94,0.18), transparent 28%),
      linear-gradient(135deg, rgba(17,24,39,0.95), rgba(15,23,42,0.82));
    border: 1px solid rgba(148,163,184,0.14);
    box-shadow: 0 18px 50px rgba(0,0,0,0.26);
  }

  .landing-badge,
  .market-hero-badge,
  .daily-badge,
  .stock-hero-badge,
  .tools-hero-badge {
    display: inline-block;
    margin-bottom: 14px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    color: #cbd5e1;
    font-size: 13px;
    letter-spacing: .08em;
  }

  .landing-hero h1,
  .market-hero h1,
  .daily-hero h1,
  .stock-hero h1,
  .tools-hero h1 {
    margin: 0;
    font-size: 38px;
    line-height: 1.2;
    color: #ffffff;
  }

  .landing-subtitle {
    margin-top: 14px;
    max-width: 760px;
    color: #dbe7f7;
    line-height: 1.8;
    font-size: 16px;
  }

  .landing-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 20px;
  }

  .cta-primary,
  .cta-secondary {
    text-decoration: none;
    padding: 12px 18px;
    border-radius: 18px;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .cta-primary {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
  }

  .cta-secondary {
    background: rgba(255,255,255,0.08);
    color: #e5eefc;
    border: 1px solid rgba(148,163,184,0.18);
  }

  .feature-showcase {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-bottom: 18px;
  }

  .feature-card {
    padding: 18px;
    border-radius: 28px 16px 28px 16px;
    border: 1px solid rgba(148,163,184,0.10);
    box-shadow: 0 12px 28px rgba(0,0,0,0.18);
  }

  .feature-card a {
    color: #fff;
  }

  .feature-card-a { background: linear-gradient(135deg, rgba(37,99,235,0.28), rgba(30,41,59,0.88)); }
  .feature-card-b { background: linear-gradient(135deg, rgba(34,197,94,0.22), rgba(30,41,59,0.88)); }
  .feature-card-c { background: linear-gradient(135deg, rgba(245,158,11,0.22), rgba(30,41,59,0.88)); }
  .feature-card-d { background: linear-gradient(135deg, rgba(236,72,153,0.22), rgba(30,41,59,0.88)); }

  .feature-icon {
    font-size: 28px;
    margin-bottom: 10px;
  }

  .feature-title {
    font-size: 18px;
    font-weight: bold;
    color: white;
    margin-bottom: 8px;
  }

  .feature-text {
    color: #dbe7f7;
    line-height: 1.7;
    margin-bottom: 12px;
  }

  .status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
  }

  .status-pill {
    background: rgba(11,18,32,0.72);
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 999px;
    padding: 14px 16px;
  }

  .status-label {
    font-size: 12px;
    color: #9fb0c7;
    margin-bottom: 6px;
  }

  .status-value {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
  }

  .landing-summary-grid,
  .stock-kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 14px;
  }

  .summary-bubble,
  .stock-kpi {
    min-height: 128px;
    border-radius: 32px 20px 32px 20px;
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    color: white;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
  }

  .summary-bubble-label,
  .stock-kpi-label {
    font-size: 13px;
    margin-bottom: 10px;
    opacity: .92;
  }

  .summary-bubble-value,
  .stock-kpi-value {
    font-size: 28px;
    font-weight: bold;
  }

  .bubble-green, .stock-kpi-green { background: linear-gradient(135deg, #16a34a, #15803d); }
  .bubble-yellow, .stock-kpi-yellow { background: linear-gradient(135deg, #f59e0b, #d97706); }
  .bubble-red, .stock-kpi-red { background: linear-gradient(135deg, #ef4444, #dc2626); }
  .bubble-blue, .stock-kpi-blue { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
  .bubble-purple, .stock-kpi-purple { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
  .bubble-orange, .stock-kpi-orange { background: linear-gradient(135deg, #fb923c, #ea580c); }
  .bubble-pink, .stock-kpi-pink { background: linear-gradient(135deg, #ec4899, #db2777); }
  .stock-kpi-indigo { background: linear-gradient(135deg, #4f46e5, #4338ca); }

  .guide-steps {
    display: grid;
    gap: 14px;
  }

  .guide-step {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    background: rgba(11,18,32,0.66);
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 24px 14px 24px 14px;
    padding: 14px;
  }

  .guide-step-no {
    min-width: 52px;
    height: 52px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(37,99,235,0.28), rgba(236,72,153,0.24));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
  }

  .guide-step-title {
    font-weight: bold;
    color: white;
    margin-bottom: 6px;
  }

  .guide-step-text {
    color: #dbe7f7;
    line-height: 1.7;
  }

  .market-hero,
  .daily-hero,
  .stock-hero,
  .tools-hero {
    position: relative;
    overflow: hidden;
    padding: 28px 24px;
    margin-bottom: 18px;
    border-radius: 30px 18px 30px 18px;
    border: 1px solid rgba(148,163,184,0.14);
    box-shadow: 0 18px 50px rgba(0,0,0,0.22);
  }

  .market-hero {
    background:
      radial-gradient(circle at 15% 20%, rgba(34,197,94,0.22), transparent 24%),
      radial-gradient(circle at 85% 20%, rgba(59,130,246,0.20), transparent 24%),
      radial-gradient(circle at 50% 100%, rgba(245,158,11,0.18), transparent 28%),
      linear-gradient(135deg, rgba(17,24,39,0.96), rgba(15,23,42,0.84));
  }

  .daily-hero {
    background:
      radial-gradient(circle at 15% 20%, rgba(168,85,247,0.22), transparent 24%),
      radial-gradient(circle at 85% 20%, rgba(34,197,94,0.18), transparent 24%),
      radial-gradient(circle at 50% 100%, rgba(245,158,11,0.18), transparent 28%),
      linear-gradient(135deg, rgba(17,24,39,0.96), rgba(15,23,42,0.84));
  }

  .stock-hero {
    background:
      radial-gradient(circle at 15% 20%, rgba(59,130,246,0.24), transparent 24%),
      radial-gradient(circle at 85% 20%, rgba(236,72,153,0.20), transparent 24%),
      radial-gradient(circle at 50% 100%, rgba(168,85,247,0.18), transparent 28%),
      linear-gradient(135deg, rgba(17,24,39,0.96), rgba(15,23,42,0.84));
  }

  .tools-hero {
    background:
      radial-gradient(circle at 15% 20%, rgba(251,146,60,0.22), transparent 24%),
      radial-gradient(circle at 85% 20%, rgba(59,130,246,0.20), transparent 24%),
      radial-gradient(circle at 50% 100%, rgba(34,197,94,0.18), transparent 28%),
      linear-gradient(135deg, rgba(17,24,39,0.96), rgba(15,23,42,0.84));
  }

  .market-summary-card {
    border-radius: 28px 18px 28px 18px;
  }

  .market-status-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
  }

  .market-status-chip {
    background: rgba(11,18,32,0.72);
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 999px;
    padding: 14px 16px;
  }

  .market-status-label {
    font-size: 12px;
    color: #9fb0c7;
    margin-bottom: 6px;
  }

  .market-status-value {
    font-size: 15px;
    font-weight: 600;
    color: white;
  }

  .market-bubble-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
  }

  .market-bubble {
    min-height: 130px;
    border-radius: 30px 18px 30px 18px;
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    color: white;
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
  }

  .market-bubble-label {
    font-size: 13px;
    margin-bottom: 10px;
    opacity: .92;
  }

  .market-bubble-value {
    font-size: 30px;
    font-weight: bold;
  }

  .market-bubble-green { background: linear-gradient(135deg, #16a34a, #15803d); }
  .market-bubble-yellow { background: linear-gradient(135deg, #f59e0b, #d97706); }
  .market-bubble-red { background: linear-gradient(135deg, #ef4444, #dc2626); }
  .market-bubble-blue { background: linear-gradient(135deg, #2563eb, #1d4ed8); }

  .market-section,
  .stock-section,
  .tools-result-card,
  .tools-empty-card {
    overflow: hidden;
  }

  .market-section-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }

  .market-section-tag {
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: bold;
  }

  .buy-tag {
    background: rgba(34,197,94,0.18);
    color: #86efac;
    border: 1px solid rgba(34,197,94,0.28);
  }

  .hold-tag {
    background: rgba(245,158,11,0.18);
    color: #fcd34d;
    border: 1px solid rgba(245,158,11,0.28);
  }

  .sell-tag {
    background: rgba(239,68,68,0.18);
    color: #fca5a5;
    border: 1px solid rgba(239,68,68,0.28);
  }

  .suitable-tag {
    background: rgba(59,130,246,0.18);
    color: #93c5fd;
    border: 1px solid rgba(59,130,246,0.28);
  }

  .market-section-buy {
    border-left: 4px solid rgba(34,197,94,0.75);
    border-radius: 28px 16px 28px 16px;
  }

  .market-section-hold {
    border-left: 4px solid rgba(245,158,11,0.75);
    border-radius: 16px 28px 16px 28px;
  }

  .market-section-sell {
    border-left: 4px solid rgba(239,68,68,0.75);
    border-radius: 28px 16px 28px 16px;
  }

  .market-section-suitable {
    border-left: 4px solid rgba(59,130,246,0.75);
    border-radius: 16px 28px 16px 28px;
  }

  .stock-item-buy {
    border: 1px solid rgba(34,197,94,0.18);
    background: linear-gradient(180deg, rgba(16,44,30,0.42), rgba(11,18,32,0.76));
  }

  .stock-item-hold {
    border: 1px solid rgba(245,158,11,0.18);
    background: linear-gradient(180deg, rgba(60,35,8,0.40), rgba(11,18,32,0.76));
  }

  .stock-item-sell {
    border: 1px solid rgba(239,68,68,0.18);
    background: linear-gradient(180deg, rgba(58,16,16,0.40), rgba(11,18,32,0.76));
  }

  .stock-item-suitable {
    border: 1px solid rgba(59,130,246,0.18);
    background: linear-gradient(180deg, rgba(14,34,67,0.40), rgba(11,18,32,0.76));
  }

  .stock-score-buy {
    background: rgba(34,197,94,0.16);
    border: 1px solid rgba(34,197,94,0.22);
    color: #86efac;
  }

  .stock-score-hold {
    background: rgba(245,158,11,0.16);
    border: 1px solid rgba(245,158,11,0.22);
    color: #fcd34d;
  }

  .stock-score-sell {
    background: rgba(239,68,68,0.16);
    border: 1px solid rgba(239,68,68,0.22);
    color: #fca5a5;
  }

  .stock-score-suitable {
    background: rgba(59,130,246,0.16);
    border: 1px solid rgba(59,130,246,0.22);
    color: #93c5fd;
  }

  .stock-overview-card {
    border-radius: 28px 16px 28px 16px;
  }

  .stock-section-a { border-left: 4px solid rgba(59,130,246,0.75); border-radius: 28px 16px 28px 16px; }
  .stock-section-b { border-left: 4px solid rgba(34,197,94,0.75); border-radius: 16px 28px 16px 28px; }
  .stock-section-c { border-left: 4px solid rgba(168,85,247,0.75); border-radius: 28px 16px 28px 16px; }
  .stock-section-d { border-left: 4px solid rgba(239,68,68,0.75); border-radius: 16px 28px 16px 28px; }
  .stock-section-e { border-left: 4px solid rgba(245,158,11,0.75); border-radius: 28px 16px 28px 16px; }
  .stock-section-f { border-left: 4px solid rgba(34,197,94,0.75); border-radius: 16px 28px 16px 28px; }
  .stock-section-g { border-left: 4px solid rgba(236,72,153,0.75); border-radius: 28px 16px 28px 16px; }

  .news-card {
    border: 1px solid rgba(236,72,153,0.16);
    background: linear-gradient(180deg, rgba(53,19,45,0.26), rgba(11,18,32,0.76));
  }

  .tools-form-card {
    border-radius: 30px 18px 30px 18px;
  }

  .tools-form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
  }

  .chart-box {
    margin-top: 16px;
    background: rgba(11,18,32,0.74);
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 22px;
    padding: 16px;
  }

  .chart-title {
    color: #dbeafe;
    font-weight: bold;
    margin-bottom: 12px;
  }

  .mode-card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-bottom: 18px;
  }

  .mode-card {
    text-align: left;
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 28px 16px 28px 16px;
    padding: 18px;
    background: rgba(15,23,42,0.78);
    color: white;
    cursor: pointer;
    transition: all .2s ease;
    box-shadow: 0 10px 22px rgba(0,0,0,0.16);
  }

  .mode-card:hover {
    transform: translateY(-2px);
  }

  .mode-card-active {
    outline: 2px solid rgba(255,255,255,0.18);
    transform: translateY(-2px);
  }

  .risk-mode {
    background: linear-gradient(135deg, rgba(59,130,246,0.28), rgba(17,24,39,0.88));
  }

  .industry-mode {
    background: linear-gradient(135deg, rgba(34,197,94,0.24), rgba(17,24,39,0.88));
  }

  .fixed-mode {
    background: linear-gradient(135deg, rgba(245,158,11,0.24), rgba(17,24,39,0.88));
  }

  .mode-card-icon {
    font-size: 28px;
    margin-bottom: 10px;
  }

  .mode-card-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
    color: white;
  }

  .mode-card-text {
    color: #dbe7f7;
   line-height: 1.7;
    font-size: 14px;
  }

  .mode-panel {
    margin-top: 12px;
    padding: 16px;
    border-radius: 24px;
    background: rgba(11,18,32,0.52);
    border: 1px solid rgba(148,163,184,0.08);
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

    .company-name { font-size: 24px; }
    .mini-value { font-size: 20px; }
    .section-title { font-size: 18px; }

    .summary-bubble,
    .market-bubble,
    .stock-kpi {
      min-height: 108px;
      border-radius: 24px 16px 24px 16px;
    }
  }
</style>
"""