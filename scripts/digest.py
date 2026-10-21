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
2. Recent News Headliners: {json.dumps(news)}

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
2. `### 📈 Core Asset Snapshot Table`: The structured table following the strict rules above.
3. `### ⚡ Sector Movers & Bellwether Divergence`: Deep-dive into notable outperformers/underperformers based on the data.
4. `### 🎯 Strategic Takeaways & Key Watchlist`: Key catalysts ahead and actionable institutional insights.

Return ONLY valid Markdown content.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.5, "maxOutputTokens": 3000}}
    
    # 自动重试机制：最多尝试 3 次
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=90)
            if resp.status_code == 200:
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Attempt {attempt + 1} failed with status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"Attempt {attempt + 1} encountered an error: {e}")
            
        # 如果不是最后一次尝试，则等待后重试
        if attempt < max_retries - 1:
            sleep_time = 15 * (attempt + 1) # 第一次等15秒，第二次等30秒
            print(f"Waiting {sleep_time} seconds before retrying...")
            time.sleep(sleep_time)
            
    # 如果 3 次全失败，则抛出异常
    raise RuntimeError("Gemini API failed after 3 attempts due to high demand or network errors.")
