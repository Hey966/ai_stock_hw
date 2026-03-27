LIVE_SCRIPT = """
<script>
function esc(v) {
  if (v === null || v === undefined) return "N/A";
  return String(v);
}

function stockCard(item, showReason = false, showMa20 = false) {
  return `
    <div class="stock-item">
      <div class="stock-head">
        <div>
          <div class="stock-name">${esc(item.company_name)}</div>
          <div class="stock-symbol">${esc(item.symbol)}｜${esc(item.suggestion)}</div>
        </div>
        <div class="stock-score">分數 ${esc(item.score)}</div>
      </div>

      <div class="stock-meta">
        <div class="stock-meta-box">
          <div class="stock-meta-label">最新價</div>
          <div class="stock-meta-value">${esc(item.latest_price)}</div>
        </div>
        <div class="stock-meta-box">
          <div class="stock-meta-label">合理價</div>
          <div class="stock-meta-value">${esc(item.fair_value)}</div>
        </div>
        ${showMa20 ? `
        <div class="stock-meta-box">
          <div class="stock-meta-label">MA20</div>
          <div class="stock-meta-value">${esc(item.ma20)}</div>
        </div>
        ` : ""}
      </div>

      ${showReason ? `<div class="stock-reason">${esc(item.reason)}</div>` : ""}
    </div>
  `;
}

function setHTML(id, html) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = html;
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = value;
}

async function refreshMarket() {
  try {
    const res = await fetch("/api/market-data", { cache: "no-store" });
    const data = await res.json();

    // 首頁：市場摘要
    setText("home-market-buy-count", (data.buy || []).length);
    setText("home-market-hold-count", (data.hold || []).length);
    setText("home-market-sell-count", (data.sell || []).length);
    setText("home-market-suitable-count", (data.suitable || []).length);
    setText("home-market-updated-at", data.updated_at || "N/A");
    setText("home-market-progress", `${data.progress?.processed || 0} / ${data.progress?.total || 0}`);
    setText("home-market-last-symbol", data.progress?.last_symbol || "-");

    // 市場頁：買入區
    if (document.getElementById("market-buy")) {
      let html = "";
      (data.buy || []).forEach(item => {
        html += stockCard(item, false, false);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無買入區名單。</div></div>';
      }
      setHTML("market-buy", html);
    }

    // 市場頁：持有區
    if (document.getElementById("market-hold")) {
      let html = "";
      (data.hold || []).forEach(item => {
        html += stockCard(item, false, false);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無持有區名單。</div></div>';
      }
      setHTML("market-hold", html);
    }

    // 市場頁：賣出區
    if (document.getElementById("market-sell")) {
      let html = "";
      (data.sell || []).forEach(item => {
        html += stockCard(item, false, false);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無賣出區名單。</div></div>';
      }
      setHTML("market-sell", html);
    }

    // 市場頁：適合區
    if (document.getElementById("market-suitable")) {
      let html = "";
      (data.suitable || []).forEach(item => {
        html += stockCard(item, false, false);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無適合區名單。</div></div>';
      }
      setHTML("market-suitable", html);
    }

    // 市場頁摘要
    setText("market-updated-at", data.updated_at || "N/A");
    setText("market-progress", `${data.progress?.processed || 0} / ${data.progress?.total || 0}`);
    setText("market-last-symbol", data.progress?.last_symbol || "-");
    setText("market-buy-count", (data.buy || []).length);
    setText("market-hold-count", (data.hold || []).length);
    setText("market-sell-count", (data.sell || []).length);
    setText("market-suitable-count", (data.suitable || []).length);

  } catch (e) {
    console.log("市場更新失敗", e);
  }
}

async function refreshDaily() {
  try {
    const res = await fetch("/api/daily-selection", { cache: "no-store" });
    const data = await res.json();

    // 首頁：今日策略摘要
    setText("home-daily-date", data.date || "N/A");
    setText("home-daily-updated-at", data.updated_at || "N/A");
    setText("home-top-buy-count", data.summary?.top_buy_count || 0);
    setText("home-watch-count", data.summary?.watch_hold_count || 0);
    setText("home-risk-count", data.summary?.risk_list_count || 0);

    // 首頁：Top Buy 預覽
    if (document.getElementById("daily-top")) {
      let html = "";
      (data.top_buy || []).slice(0, 5).forEach(item => {
        html += stockCard(item, false, false);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無 Top Buy 名單。</div></div>';
      }
      setHTML("daily-top", html);
    }

    // 今日頁摘要
    setText("daily-date", data.date || "N/A");
    setText("daily-updated-at", data.updated_at || "N/A");
    setText("daily-top-count", data.summary?.top_buy_count || 0);
    setText("daily-watch-count", data.summary?.watch_hold_count || 0);
    setText("daily-risk-count", data.summary?.risk_list_count || 0);

    // 今日頁：Top Buy
    if (document.getElementById("daily-top-full")) {
      let html = "";
      (data.top_buy || []).forEach(item => {
        html += stockCard(item, true, true);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無 Top Buy 名單。</div></div>';
      }
      setHTML("daily-top-full", html);
    }

    // 今日頁：觀察
    if (document.getElementById("daily-watch")) {
      let html = "";
      (data.watch_hold || []).forEach(item => {
        html += stockCard(item, true, true);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無今日觀察名單。</div></div>';
      }
      setHTML("daily-watch", html);
    }

    // 今日頁：風險
    if (document.getElementById("daily-risk")) {
      let html = "";
      (data.risk_list || []).forEach(item => {
        html += stockCard(item, true, true);
      });
      if (!html) {
        html = '<div class="info-item"><div class="value">目前尚無今日風險名單。</div></div>';
      }
      setHTML("daily-risk", html);
    }

  } catch (e) {
    console.log("每日策略更新失敗", e);
  }
}

function autoUpdate() {
  console.log("更新中...", new Date().toLocaleTimeString());
  refreshMarket();
  refreshDaily();
}

// 載入後先更新一次
document.addEventListener("DOMContentLoaded", autoUpdate);

// 每 5 秒更新一次
setInterval(autoUpdate, 5000);
</script>
"""