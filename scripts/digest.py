import os
import json
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
import pandas as pd
import time

# 强制 matplotlib 在无 GUI 的服务器环境下运行
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

WATCHLIST = {
    "indices": {"^GSPC": "S&P 500", "^IXIC": "Nasdaq Composite", "^DJI": "Dow Jones"},
    "commodities": {"BZ=F": "Brent Crude Oil", "GC=F": "Gold Futures (London Gold)"},
    "bellwethers": {
        "NVDA": "Nvidia (AI/Semis)", "AAPL": "Apple (Consumer Tech)", 
        "MSFT": "Microsoft (Cloud/Enterprise)", "AMZN": "Amazon (E-Commerce/Cloud)", 
        "TSLA": "Tesla (EV/Autonomous)", "TSM": "TSMC (Chip Foundry)", 
        "JPM": "JPMorgan Chase (Financials)", "LLY": "Eli Lilly (Pharma/Healthcare)", 
        "XOM": "ExxonMobil (Energy)"
    }
}

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "_data", "market_summary.json")

def detect_market_phase():
    ny_now = datetime.now(ZoneInfo("America/New_York"))
    if ny_now.weekday() >= 5:
        print(f"[{ny_now}] Weekend detected. Market closed. Exiting.")
        return None, ny_now

    current_minute = ny_now.hour * 60 + ny_now.minute
    
    # 无缝衔接时间窗，防止排队延迟导致数据落入 manual_run 分支
    if 530 <= current_minute <= 569:
        return "pre_market", ny_now
    elif 570 <= current_minute <= 769:
        return "market_open", ny_now
    elif 770 <= current_minute <= 959:
        return "mid_day", ny_now
    elif 960 <= current_minute <= 1020:
        return "market_close", ny_now
    else:
        print(f"[{ny_now}] Outside preset time windows. Defaulting to manual inspection mode.")
        return "manual_run", ny_now

def harvest_market_data():
    all_tickers = list(WATCHLIST["indices"].keys()) + list(WATCHLIST["commodities"].keys()) + list(WATCHLIST["bellwethers"].keys())
    data = yf.download(all_tickers, period="2d", interval="1d", progress=False)
    
    metrics = []
    for ticker in all_tickers:
        try:
            # 兼容不同版本 yfinance 返回的列结构
            if isinstance(data["Close"], pd.DataFrame):
                close_series = data["Close"][ticker].dropna()
            else:
                close_series = data["Close"].dropna()
                
            if len(close_series) >= 2:
                prev_close = float(close_series.iloc[-2])
                curr_price = float(close_series.iloc[-1])
                chg_pct = ((curr_price - prev_close) / prev_close) * 100
            else:
                curr_price = float(close_series.iloc[-1])
                chg_pct = 0.0
            
            name = WATCHLIST["indices"].get(ticker) or WATCHLIST["commodities"].get(ticker) or WATCHLIST["bellwethers"].get(ticker)
            metrics.append({"ticker": ticker, "name": name, "price": round(curr_price, 2), "change_pct": round(chg_pct, 2)})
        except Exception as e:
            continue

    news_items = []
    primary_tickers = ["^GSPC", "NVDA", "AAPL", "TSLA"]
    for sym in primary_tickers:
        try:
            t = yf.Ticker(sym)
            for item in (t.news or [])[:2]:
                title = item.get("title")
                if title and title not in [n["title"] for n in news_items]:
                    news_items.append({"title": title, "publisher": item.get("publisher", "Financial Wire")})
        except Exception:
            continue

    return metrics, news_items[:8]

def generate_nasdaq_chart(ny_now):
    try:
        # 获取纳指当天的 5 分钟线数据
        data = yf.download("^IXIC", period="1d", interval="5m", progress=False)
        if data.empty:
            return ""
        
        # 兼容最新版 yfinance 的多层索引结构
        if 'Close' in data:
            if isinstance(data['Close'], pd.DataFrame) and "^IXIC" in data['Close'].columns:
                close_series = data['Close']["^IXIC"]
            else:
                close_series = data['Close']
        else:
            return ""

        plt.figure(figsize=(9, 4))
        plt.plot(close_series.index, close_series.values, color='#4a90e2', linewidth=2.5)
        
        plt.title(f"Nasdaq Composite (^IXIC) Intraday - {ny_now.strftime('%b %d, %Y')}", fontsize=13, fontweight='bold', color='#2c3e50')
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.ylabel("Index Value")
        plt.tight_layout()
        
        # 确保图片保存路径存在
        chart_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "charts")
        os.makedirs(chart_dir, exist_ok=True)
        chart_filename = "nasdaq_intraday.png"
        chart_path = os.path.join(chart_dir, chart_filename)
        
        plt.savefig(chart_path, dpi=150, transparent=True)
        plt.close()
        
        # 利用时间戳参数防止 GitHub Pages 和浏览器缓存旧图片
        timestamp = int(ny_now.timestamp())
        return f"\n\n### 📈 Real-Time Nasdaq Intraday Chart\n![Nasdaq Chart](/assets/charts/{chart_filename}?t={timestamp})\n"
    except Exception as e:
        print(f"Chart generation failed: {e}")
        return ""

def generate_ai_analysis(phase, ny_now, metrics, news):
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise ValueError("Missing LLM_API_KEY environment variable!")

    phase_titles = {
        "pre_market": "Pre-Market Macro & Catalyst Briefing",
        "market_open": "Opening Bell Pulse & Early Action",
        "mid_day": "Mid-Day Liquidity & Sector Rotation Review",
        "market_close": "Closing Bell Comprehensive Wrap",
        "manual_run": "On-Demand Market Intelligence Report"
    }
    
    prompt = f"""
You are an institutional macro strategist and equity analyst on Wall Street. 
Generate a highly detailed, comprehensive, and structured executive financial digest in English based on the provided raw data.

Session Phase: {phase_titles.get(phase, "Market Report")}
Timestamp: {ny_now.strftime('%Y-%m-%d %H:%M:%S %Z')}

Input Snapshot:
1. Asset Metrics: {json.dumps(metrics)}
​2. Recent News Headliners: {json.dumps(news)}

STRICT Formatting & Depth Requirements:
- CRITICAL DEPTH: Provide IN-DEPTH analysis. Sections 1, 3, and 4 MUST each contain at least 2 to 3 robust, insightful paragraphs. Expand thoroughly on macro implications, rate expectations, sector rotations, and news sentiment. Do NOT write single short sentences.
- Use rich Markdown styling: Emojis (📊, 🟢, 🔴, ⚠️, ⚡, 💡), **bold** key terms, and `code highlight` for tickers.
- CRITICAL TABLE FORMAT (DO NOT BREAK THIS): You MUST leave one completely empty line BEFORE and AFTER the table. You MUST use standard hyphens (-) for dividers, NEVER use em-dashes (—). 
  Correct Table Example:
  
  | Asset | Symbol | Price | Chg % | Signal |
  |---|---|---|---|---|
  | S&P 500 | `^GSPC` | 5000.00 | +1.20% | 🟢 Bullish |

Structure exactly into these four sections:
1. `### 🌐 Executive Macro & Market Regime`: Thorough 3-paragraph analysis of broader sentiment, index trends, and macro backdrop.
​2. `### 📈 Core Asset Snapshot Table`: The structured table following the strict rules above.
3. `### ⚡ Sector Movers & Bellwether Divergence`: Deep-dive into notable outperformers/underperformers based on the data.
4. `### 🎯 Strategic Takeaways & Key Watchlist`: Key catalysts ahead and actionable institutional insights.

Return ONLY valid Markdown content.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.5, "maxOutputTokens": 3000}}
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=90)
            if resp.status_code == 200:
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Attempt {attempt + 1} failed with status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"Attempt {attempt + 1} encountered an error: {e}")
            
        if attempt < max_retries - 1:
            sleep_time = 15 * (attempt + 1) # 等待时间依次递增：15秒, 30秒, 45秒, 60秒
            print(f"Waiting {sleep_time} seconds before retrying...")
            time.sleep(sleep_time)
            
    raise RuntimeError(f"Gemini API failed after {max_retries} attempts due to high demand or network errors.")

def update_json_store(phase, ny_now, analysis_content):
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    today_str = ny_now.strftime("%Y-%m-%d")
    data_store = {"last_updated": ny_now.strftime("%Y-%m-%d %H:%M:%S %Z"), "date": today_str, "phases": {}}

    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
                if existing.get("date") == today_str:
                    data_store["phases"] = existing.get("phases", {})
        except Exception:
            pass

    data_store["phases"][phase] = {"timestamp": ny_now.strftime("%H:%M:%S %Z"), "content": analysis_content}
    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data_store, f, indent=2, ensure_ascii=False)

def main():
    phase, ny_now = detect_market_phase()
    if not phase:
        return

    print("Fetching market data and news...")
    metrics, news = harvest_market_data()

    print("Generating Intraday Chart...")
    chart_markdown = generate_nasdaq_chart(ny_now)

    print("Requesting Gemini analysis...")
    analysis = generate_ai_analysis(phase, ny_now, metrics, news)

    # 组合 AI 文本与真实的图表 Markdown
    final_content = analysis + chart_markdown

    print("Writing results...")
    update_json_store(phase, ny_now, final_content)

if __name__ == "__main__":
    main()
