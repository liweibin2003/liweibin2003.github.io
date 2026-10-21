---
title: US Market Radar
subtitle: Automated institutional market intelligence powered by Python & Gemini AI.
layout: "page"
icon: fa-chart-line
order: 3
---

{% assign market = site.data.market_summary %}

<style>
  .market-meta-bar {
    background: #f4f6f8;
    border-left: 4px solid #4a90e2;
    padding: 12px 18px;
    margin-bottom: 25px;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    font-size: 0.9em;
  }
  .phase-card {
    background: #ffffff;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    padding: 20px 24px;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  }
  .phase-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #f0f2f5;
    padding-bottom: 10px;
    margin-bottom: 15px;
  }
  .phase-title {
    margin: 0;
    font-size: 1.25em;
    font-weight: 700;
  }
  .phase-badge {
    background: #e8f4fd;
    color: #1b65d4;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: 600;
  }
  .phase-pending {
    background: #fafbfc;
    border: 1px dashed #d0d7de;
    padding: 20px;
    text-align: center;
    color: #656d76;
    border-radius: 6px;
    margin-bottom: 25px;
  }
  /* 确保生成的表格横向自适应滚动 */
  .phase-card table {
    width: 100%;
    display: table;
    margin: 15px 0;
  }
</style>

<div class="market-meta-bar">
  <div><strong>Trading Date:</strong> {{ market.date | default: "Syncing..." }} (US/Eastern)</div>
  <div><strong>Last Pipeline Run:</strong> {{ market.last_updated | default: "Pending first run" }}</div>
</div>

<!-- ================= PHASE 1: PRE-MARKET ================= -->
{% if market.phases.pre_market %}
<div class="phase-card">
  <div class="phase-header">
    <div class="phase-title">🌅 Pre-Market Macro & Catalysts</div>
    <span class="phase-badge">{{ market.phases.pre_market.timestamp }}</span>
  </div>
  <div class="phase-body">
    {{ market.phases.pre_market.content | markdownify }}
  </div>
</div>
{% else %}
<div class="phase-pending">
  ⏳ <strong>09:00 AM ET Session</strong>: Pre-market digest will generate before market open.
</div>
{% endif %}

<!-- ================= PHASE 2: OPENING BELL ================= -->
{% if market.phases.market_open %}
<div class="phase-card">
  <div class="phase-header">
    <div class="phase-title">🔔 Opening Bell Pulse (First 5 Mins)</div>
    <span class="phase-badge">{{ market.phases.market_open.timestamp }}</span>
  </div>
  <div class="phase-body">
    {{ market.phases.market_open.content | markdownify }}
  </div>
</div>
{% else %}
<div class="phase-pending">
  ⏳ <strong>09:35 AM ET Session</strong>: Opening auction volatility analysis pending.
</div>
{% endif %}

<!-- ================= PHASE 3: MID-DAY REVIEW ================= -->
{% if market.phases.mid_day %}
<div class="phase-card">
  <div class="phase-header">
    <div class="phase-title">☀️ Mid-Day Sector & Flow Review</div>
    <span class="phase-badge">{{ market.phases.mid_day.timestamp }}</span>
  </div>
  <div class="phase-body">
    {{ market.phases.mid_day.content | markdownify }}
  </div>
</div>
{% else %}
<div class="phase-pending">
  ⏳ <strong>01:00 PM ET Session</strong>: Mid-day institutional liquidity digest pending.
</div>
{% endif %}

<!-- ================= PHASE 4: CLOSING BELL ================= -->
{% if market.phases.market_close %}
<div class="phase-card">
  <div class="phase-header">
    <div class="phase-title">🌙 Closing Bell Wrap & Risk Assessment</div>
    <span class="phase-badge">{{ market.phases.market_close.timestamp }}</span>
  </div>
  <div class="phase-body">
    {{ market.phases.market_close.content | markdownify }}
  </div>
</div>
{% else %}
<div class="phase-pending">
  ⏳ <strong>04:05 PM ET Session</strong>: Final closing wrap & next-day outlook pending.
</div>
{% endif %}
