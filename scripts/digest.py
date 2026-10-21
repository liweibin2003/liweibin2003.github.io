import os
import json
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf

# 1. 核心配置与资产清单
WATCHLIST = {
    "indices": {
        "^GSPC": "S&P 500",
        "^IXIC": "Nasdaq Composite",
        "^DJI": "Dow Jones"
    },
    "commodities": {
        "BZ=F": "Brent Crude Oil",
        "GC=F": "Gold Futures (London Gold Proxy)"
    },
    "bellwethers": {
        "NVDA": "Nvidia (AI/Semis)",
        "AAPL": "Apple (Consumer Tech)",
        "MSFT": "Microsoft (Cloud/Enterprise)",
        "AMZN": "Amazon (E-Commerce/Cloud)",
        "TSLA": "Tesla (EV/Autonomous)",
        "TSM": "TSMC (Chip Foundry)",
        "JPM": "JPMorgan Chase (Financials)",
        "LLY": "Eli Lilly (Pharma/Healthcare)",
        "XOM": "ExxonMobil (Energy)"
    }
}

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "_data", "market_summary.json")

# 2. 判断纽约时间与运行阶段 (兼容夏令时/冬令时)
def detect_market_phase():
    ny_now = datetime.now(ZoneInfo("America/New_York"))
    
    # 过滤周末 (周六=5, 周日=6)
    if ny_now.weekday() >= 5:
        print(f"[{ny_now}] Weekend detected. Market closed. Exiting.")
        return None, ny_now

    current_minute = ny_now.hour * 60 + ny_now.minute

    # 定义4个阶段的时间容差窗口 (美东时间)
    # 09:00 -> 540m (允许 08:50 - 09:15)
    # 09:35 -> 575m (允许 09:30 - 09:50)
    # 13:00 -> 780m (允许 12:50 - 13:15)
    # 16:05 -> 965m (允许 16:00 - 16:25)
    if 530 <= current_minute <= 555:
        return "pre_market", ny_now
    elif 570 <= current_minute <= 590:
        return "market_open", ny_now
    elif 770 <= current_minute <= 795:
        return "mid_day", ny_now
    elif 960 <= current_minute <= 985:
        return "market_close", ny_now
    else:
        # 如果是手动触发或测试，默认设置为最近或当前的阶段
        print(f"[{ny_now}] Outside preset time windows. Defaulting to manual inspection mode.")
        return "manual_run", ny_now

# 3. 提取行情与精选新闻
def harvest_market_data():
    all_tickers = (
        list(WATCHLIST["indices"].keys()) +
        list(WATCHLIST["commodities"].keys()) +
        list(WATCHLIST["bellwethers"].keys())
    )
    
    data = yf.download(all_tickers, period="2d", interval="1d", progress=False)
    
    metrics = []
    for ticker in all_tickers:
        try:
            close_series = data["Close"][ticker].dropna()
            if len(close_series) >= 2:
                prev_close = close_series.iloc[-2]
                curr_price = close_series.iloc[-1]
                chg_pct = ((curr_price - prev_close) / prev_close) * 100
            else:
                curr_price = close_series.iloc[-1]
                chg_pct = 0.0
            
            name = (
                WATCHLIST["indices"].get(ticker) or 
                WATCHLIST["commodities"].get(ticker) or 
                WATCHLIST["bellwethers"].get(ticker)
            )
            metrics.append({
                "ticker": ticker,
                "name": name,
                "price": round(curr_price, 2),
                "change_pct": round(chg_pct, 2)
            })
        except Exception as e:
            print(f"Error parsing {ticker}: {e}")

    # 抓取具有代表性的财经要闻
    news_items = []
    primary_tickers = ["^GSPC", "NVDA", "AAPL", "TSLA"]
    for sym in primary_tickers:
        try:
            t = yf.Ticker(sym)
            for item in (t.news or [])[:2]:
                title = item.get("title")
                publisher = item.get("publisher", "Financial Wire")
                if title and title not in [n["title"] for n in news_items]:
                    news_items.append({"title": title, "publisher": publisher})
        except Exception:
            continue

    return metrics, news_items[:8]

# 4. 调用 Google AI Studio (Gemini 2.5 Flash)
def generate_ai_analysis(phase, ny_now, metrics, news):
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise ValueError("Missing LLM_API_KEY environment variable!")

    phase_titles = {
        "pre_market": "Pre-Market Macro & Catalyst Briefing (09:00 AM ET)",
        "market_open": "Opening Bell Pulse & Early Action (09:35 AM ET)",
        "mid_day": "Mid-Day Liquidity & Sector Rotation Review (01:00 PM ET)",
        "market_close": "Closing Bell Comprehensive Wrap & Risk Analysis (04:05 PM ET)",
        "manual_run": "On-Demand Market Intelligence Report"
    }
    current_title = phase_titles.get(phase, "Market Intelligence Report")

    # 构造英文专业 Prompt
    prompt = f"""
You are an institutional macro strategist and equity analyst on Wall Street. 
Generate a sharp, professional, highly structured executive financial digest in English based on the provided raw market data and news.

Session Phase: {current_title}
Timestamp: {ny_now.strftime('%Y-%m-%d %H:%M:%S %Z')}

Input Snapshot:
1. Asset Metrics: {json.dumps(metrics)}
2. Recent News Headliners: {json.dumps(news)}

Styling and Formatting Requirements:
- Write strictly in **fluent, rigorous financial English**.
- Avoid dry plain text. Use rich Markdown styling:
  * Strategic business emojis (📊, 🟢, 🔴, ⚠️, ⚡, 💡) to denote direction and asset classes.
  * Key terms in **bold** and critical warnings/takeaways in `code highlight` or *italicized emphasis*.
  * Organize the Core Asset Snapshot into a clean, compact Markdown Table: columns: `Asset`, `Symbol`, `Price`, `Chg %`, `Signal`.
- Structure the analysis into four distinct sections:
  1. `### 🌐 Executive Macro & Market Regime`: Broader sentiment, index trends, macro backdrop (rates, dollar, yields context).
  2. `### 📈 Core Asset Snapshot Table`: The structured table mentioned above.
  3. `### ⚡ Sector Movers & Bellwether Divergence`: Deep-dive into notable outperformers/underperformers among big tech, semis, energy, or financials.
  4. `### 🎯 Strategic Takeaways & Key Watchlist`: Key catalysts ahead for the next trading phase.

Make the insights concise, rigorous, and devoid of fluff. Return ONLY valid Markdown content.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048
        }
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API request failed [{resp.status_code}]: {resp.text}")

    result = resp.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

# 5. 保存到 _data/market_summary.json
def update_json_store(phase, ny_now, analysis_content):
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    today_str = ny_now.strftime("%Y-%m-%d")

    data_store = {
        "last_updated": ny_now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "date": today_str,
        "phases": {}
    }

    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
                # 如果是同一天，保留之前阶段的数据
                if existing.get("date") == today_str:
                    data_store["phases"] = existing.get("phases", {})
        except Exception:
            pass

    data_store["phases"][phase] = {
        "timestamp": ny_now.strftime("%H:%M:%S %Z"),
        "content": analysis_content
    }

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data_store, f, indent=2, ensure_ascii=False)
    print(f"Successfully recorded [{phase}] digest into {DATA_FILE_PATH}")

# 6. 主调度器
def main():
    phase, ny_now = detect_market_phase()
    if not phase:
        return

    print(f"Triggered phase: {phase} at {ny_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("Fetching market data and financial news...")
    metrics, news = harvest_market_data()

    print("Requesting Gemini 2.5 Flash analysis...")
    analysis = generate_ai_analysis(phase, ny_now, metrics, news)

    print("Writing results to Jekyll _data...")
    update_json_store(phase, ny_now, analysis)

if __name__ == "__main__":
    main()
