---
title: Web Crawler
subtitle: Multi-Platform Video Data Search
layout: "page"
icon: fa-bug
order: 5
---

<!-- Include Font Awesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
  /* Isolate styles to prevent conflict with global Jekyll themes */
  .crawler-app {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    max-width: 1000px;
    margin: 0 auto;
    color: #333;
  }

  /* Section Headers & Dividers */
  .feature-section {
    background: #ffffff;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 32px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    border: 1px solid #eaeaea;
  }
  .feature-header {
    margin-bottom: 24px;
    border-bottom: 2px solid #f5f5f5;
    padding-bottom: 16px;
  }
  .feature-header h2 {
    margin: 0 0 8px 0;
    font-size: 22px;
    color: #111;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .feature-header p {
    margin: 0;
    color: #666;
    font-size: 14px;
  }
  
  /* Platform Tabs */
  .crawler-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }
  .tab-btn {
    padding: 10px 20px;
    font-size: 15px;
    font-weight: bold;
    border: 1px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    background: #f5f5f5 !important;
    color: #333 !important;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  /* Active states for different platforms */
  .tab-btn.active-yt { background: #FF0000 !important; color: #FFF !important; border-color: #FF0000; }
  .tab-btn.active-tw { background: #9146FF !important; color: #FFF !important; border-color: #9146FF; }
  .tab-btn.active-vi { background: #1AB7EA !important; color: #FFF !important; border-color: #1AB7EA; }
  .tab-btn.active-dm { background: #0066DC !important; color: #FFF !important; border-color: #0066DC; }

  /* Input & Button Areas */
  .search-container {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
  }
  .search-input {
    flex: 1;
    padding: 12px 16px;
    font-size: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.3s;
    background: #fff;
    color: #333;
  }
  .search-input:focus { border-color: #333; }
  .search-btn {
    padding: 0 24px;
    font-size: 15px;
    font-weight: bold;
    color: #fff;
    background: #333;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s;
    white-space: nowrap;
  }
  .search-btn:hover { background: #000; }
  .search-btn:disabled { background: #ccc; cursor: not-allowed; }

  /* Dynamic Filter Panel */
  .filter-panel {
    display: none;
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    gap: 16px;
    flex-wrap: wrap;
    border: 1px solid #eee;
  }
  .filter-panel.active { display: flex; }
  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .filter-group label {
    font-size: 12px;
    font-weight: bold;
    color: #666;
    text-transform: uppercase;
  }
  .filter-group select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    background: #fff;
    color: #333;
    min-width: 150px;
  }

  /* Status Area */
  .status-area {
    text-align: center;
    padding: 30px 0;
    color: #888;
    font-size: 15px;
  }
  .spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #333;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
    margin: 0 auto 12px auto;
  }
  @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

  /* Results Grid (Data Explorer) */
  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  .video-card {
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #f0f0f0;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .video-card:hover { 
    transform: translateY(-4px); 
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  }
  .video-cover {
    width: 100%;
    aspect-ratio: 16/9;
    background: #e0e0e0;
    object-fit: cover;
    display: block;
  }
  .video-info { padding: 16px; }
  .video-title {
    font-size: 14px;
    font-weight: 600;
    margin: 0 0 10px 0;
    line-height: 1.4;
    color: #111;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .video-meta {
    font-size: 12px;
    color: #666;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  /* Parser Result Area */
  .parser-supported {
    font-size: 13px;
    color: #888;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .parser-supported i {
    font-size: 16px;
  }
  .download-result {
    margin-top: 20px;
    padding: 20px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    display: none;
    align-items: center;
    justify-content: space-between;
  }
  .download-info {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .download-thumb {
    width: 80px;
    height: 45px;
    border-radius: 4px;
    object-fit: cover;
  }
  .download-text h4 {
    margin: 0 0 4px 0;
    font-size: 15px;
    color: #166534;
  }
  .download-text p {
    margin: 0;
    font-size: 12px;
    color: #15803d;
  }
  .download-action {
    background: #16a34a;
    color: #fff;
    padding: 8px 16px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: bold;
    font-size: 14px;
    transition: background 0.2s;
  }
  .download-action:hover {
    background: #15803d;
    color: #fff;
  }

  /* Demo Notice Box */
  .demo-notice {
    margin-top: 24px;
    padding: 16px;
    background-color: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 8px;
    color: #92400e;
    font-size: 13px;
    line-height: 1.5;
    display: flex;
    align-items: flex-start;
    gap: 10px;
  }
  .demo-notice i {
    color: #d97706;
    font-size: 16px;
    margin-top: 2px;
  }
  .demo-notice code {
    background: #fef3c7;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    color: #b45309;
  }
</style>

<div class="crawler-app">

  <!-- ========================================== -->
  <!-- FEATURE 1: VIDEO DATA EXPLORER             -->
  <!-- ========================================== -->
  <div class="feature-section">
    <div class="feature-header">
      <h2><i class="fa-solid fa-chart-line"></i> Video Data Explorer</h2>
      <p>Search and analyze video metadata, views, and engagement metrics across multiple platforms.</p>
    </div>

    <!-- Platform Tabs -->
    <div class="crawler-tabs">
      <button class="tab-btn active-yt" onclick="switchPlatform('youtube')" id="tab-yt">
        <i class="fa-brands fa-youtube"></i> YouTube
      </button>
      <button class="tab-btn" onclick="switchPlatform('twitch')" id="tab-tw">
        <i class="fa-brands fa-twitch"></i> Twitch
      </button>
      <button class="tab-btn" onclick="switchPlatform('vimeo')" id="tab-vi">
        <i class="fa-brands fa-vimeo"></i> Vimeo
      </button>
      <button class="tab-btn" onclick="switchPlatform('dailymotion')" id="tab-dm">
        <i class="fa-brands fa-dailymotion"></i> Dailymotion
      </button>
    </div>

    <!-- Main Search Box -->
    <div class="search-container">
      <input type="text" id="searchInput" class="search-input" placeholder="Enter keyword, e.g., Gameplay, Trailer...">
      <button id="searchBtn" class="search-btn" onclick="fetchData()">Search Data</button>
    </div>

    <!-- Filters (YouTube) -->
    <div id="filters-youtube" class="filter-panel active">
      <div class="filter-group">
        <label>Order By</label>
        <select id="yt-order">
          <option value="viewCount">Highest Views</option>
          <option value="date">Latest Published</option>
          <option value="relevance">Relevance</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Duration</label>
        <select id="yt-duration">
          <option value="any">Any Duration</option>
          <option value="short">Short (< 4 mins)</option>
          <option value="long">Long (> 20 mins)</option>
        </select>
      </div>
    </div>

    <!-- Filters (Twitch) -->
    <div id="filters-twitch" class="filter-panel">
      <div class="filter-group">
        <label>Content Type</label>
        <select id="tw-type">
          <option value="streams">Live Streams</option>
          <option value="vods">VODs (Past Broadcasts)</option>
          <option value="clips">Clips (Highlights)</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Sort By</label>
        <select id="tw-sort">
          <option value="views">Most Views</option>
          <option value="trending">Trending Now</option>
        </select>
      </div>
    </div>

    <!-- Filters (Vimeo) -->
    <div id="filters-vimeo" class="filter-panel">
      <div class="filter-group">
        <label>Sort By</label>
        <select id="vi-sort">
          <option value="relevant">Relevance</option>
          <option value="date">Date Added</option>
          <option value="plays">Most Played</option>
          <option value="likes">Most Liked</option>
        </select>
      </div>
    </div>

    <!-- Filters (Dailymotion) -->
    <div id="filters-dailymotion" class="filter-panel">
      <div class="filter-group">
        <label>Sort By</label>
        <select id="dm-sort">
          <option value="relevance">Relevance</option>
          <option value="visited">Most Viewed</option>
          <option value="recent">Most Recent</option>
        </select>
      </div>
    </div>

    <!-- Status & Results Area -->
    <div id="statusArea" class="status-area">Waiting for search input...</div>
    <div id="resultsGrid" class="results-grid"></div>

    <!-- Demo Notice for Section 1 -->
    <div class="demo-notice">
      <i class="fa-solid fa-circle-info"></i>
      <div>
        <strong>UI Mockup / Demo Mode:</strong> The search results currently displayed are generated locally using mock data. To fetch real video metrics, you need to connect the <code>fetchData()</code> javascript function to a real Serverless API (e.g., Cloudflare Workers or Vercel) that queries the respective platform APIs.
      </div>
    </div>
  </div>


  <!-- ========================================== -->
  <!-- FEATURE 2: MEDIA PARSER & DOWNLOADER       -->
  <!-- ========================================== -->
  <div class="feature-section">
    <div class="feature-header">
      <h2><i class="fa-solid fa-cloud-arrow-down"></i> Media Parser & Downloader</h2>
      <p>Paste a video URL to extract and generate direct watermark-free download links.</p>
    </div>

    <div class="search-container">
      <input type="text" id="downloadInput" class="search-input" placeholder="Paste link here (e.g., https://www.youtube.com/watch?v=...)">
      <button id="parseBtn" class="search-btn" onclick="parseVideo()">Parse Link</button>
    </div>

    <div class="parser-supported">
      <span>Supported Platforms:</span>
      <i class="fa-brands fa-youtube" style="color: #FF0000;" title="YouTube"></i>
      <i class="fa-brands fa-tiktok" style="color: #000000;" title="TikTok"></i>
      <i class="fa-brands fa-tiktok" style="color: #FE2C55;" title="Douyin"></i> <!-- Using TikTok icon for Douyin -->
      <i class="fa-brands fa-bilibili" style="color: #00A1D6;" title="Bilibili"></i>
    </div>

    <!-- Parser Status / Result Box -->
    <div id="parseStatus" class="status-area" style="display: none; padding: 20px 0;"></div>
    
    <div id="downloadResult" class="download-result">
      <div class="download-info">
        <img id="dl-thumb" class="download-thumb" src="" alt="Thumbnail">
        <div class="download-text">
          <h4 id="dl-title">Video Title</h4>
          <p id="dl-meta">1080p MP4 • Ready to download</p>
        </div>
      </div>
      <a href="#" id="dl-link" class="download-action" target="_blank" rel="noreferrer">
        <i class="fa-solid fa-download"></i> Download Video
      </a>
    </div>

    <!-- Demo Notice for Section 2 -->
    <div class="demo-notice">
      <i class="fa-solid fa-circle-info"></i>
      <div>
        <strong>UI Mockup / Demo Mode:</strong> The generated download link is a placeholder. GitHub Pages cannot parse video streams natively. To enable actual downloading, integrate a third-party media parsing API (like Cobalt API or RapidAPI) inside the <code>parseVideo()</code> function to fetch the real <code>.mp4</code> source links.
      </div>
    </div>
  </div>

</div>

<script>
  /* =========================================================
     LOGIC FOR FEATURE 1: VIDEO DATA EXPLORER
     ========================================================= */
  let currentPlatform = 'youtube';

  function switchPlatform(platform) {
    currentPlatform = platform;
    
    document.getElementById('tab-yt').className = 'tab-btn';
    document.getElementById('tab-tw').className = 'tab-btn';
    document.getElementById('tab-vi').className = 'tab-btn';
    document.getElementById('tab-dm').className = 'tab-btn';

    if (platform === 'youtube') document.getElementById('tab-yt').classList.add('active-yt');
    if (platform === 'twitch') document.getElementById('tab-tw').classList.add('active-tw');
    if (platform === 'vimeo') document.getElementById('tab-vi').classList.add('active-vi');
    if (platform === 'dailymotion') document.getElementById('tab-dm').classList.add('active-dm');
    
    document.getElementById('filters-youtube').classList.remove('active');
    document.getElementById('filters-twitch').classList.remove('active');
    document.getElementById('filters-vimeo').classList.remove('active');
    document.getElementById('filters-dailymotion').classList.remove('active');

    document.getElementById(`filters-${platform}`).classList.add('active');
    
    document.getElementById('resultsGrid').innerHTML = '';
    document.getElementById('statusArea').style.display = 'block';
    document.getElementById('statusArea').innerHTML = 'Waiting for search input...';
  }

  function fetchData() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) {
      alert("Please enter a search keyword first!");
      return;
    }

    const btn = document.getElementById('searchBtn');
    const statusArea = document.getElementById('statusArea');
    const resultsGrid = document.getElementById('resultsGrid');
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Searching...';
    statusArea.style.display = 'block';
    statusArea.innerHTML = '<div class="spinner"></div><p>Fetching API data...</p>';
    resultsGrid.innerHTML = '';

    // Mock API fetch delay
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = 'Search Data';
      statusArea.style.display = 'none';
      const mockData = generateMockData(currentPlatform, query);
      renderResults(mockData, currentPlatform);
    }, 1200);
  }

  function renderResults(data, platform) {
    const grid = document.getElementById('resultsGrid');
    if (data.length === 0) return;

    data.forEach(item => {
      const card = document.createElement('div');
      card.className = 'video-card';
      let cardInnerHTML = `<img class="video-cover" src="${item.thumbnail}" alt="cover"><div class="video-info">`;

      if (platform === 'youtube') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta"><span>${item.channel}</span><span>${item.date}</span></div>
            <div class="video-meta"><strong style="color:#222">${item.views} Views</strong><strong><i class="fa-solid fa-thumbs-up"></i> ${item.likes}</strong></div>
        `;
      } else if (platform === 'twitch') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta"><span>${item.streamer}</span><span>${item.duration}</span></div>
            <div class="video-meta"><strong style="color:#9146FF">${item.category}</strong><strong><i class="fa-solid fa-users"></i> ${item.viewers}</strong></div>
        `;
      } else if (platform === 'vimeo') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta"><span>${item.creator}</span><span>${item.duration}</span></div>
            <div class="video-meta"><strong style="color:#1AB7EA">${item.plays} Plays</strong><strong><i class="fa-solid fa-heart"></i> ${item.likes}</strong></div>
        `;
      } else if (platform === 'dailymotion') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta"><span>${item.owner}</span><span>${item.date}</span></div>
            <div class="video-meta"><strong style="color:#0066DC">${item.views} Views</strong><strong>${item.duration}</strong></div>
        `;
      }
      cardInnerHTML += `</div>`;
      card.innerHTML = cardInnerHTML;
      grid.appendChild(card);
    });
  }

  function generateMockData(platform, query) {
    return [1, 2, 3].map(i => {
      return {
        title: `[${query}] Demo Video ${i}`,
        channel: "User " + i, streamer: "Player " + i, creator: "Studio " + i, owner: "Channel " + i,
        views: Math.floor(Math.random() * 500) + "K",
        likes: Math.floor(Math.random() * 5000),
        plays: Math.floor(Math.random() * 900) + "K",
        viewers: Math.floor(Math.random() * 20000),
        date: "2 days ago", duration: "10:30", category: query,
        thumbnail: `https://picsum.photos/seed/${query}${platform}${i}/400/225`
      };
    });
  }

  /* =========================================================
     LOGIC FOR FEATURE 2: MEDIA PARSER & DOWNLOADER
     ========================================================= */
  function parseVideo() {
    const url = document.getElementById('downloadInput').value.trim();
    if (!url) {
      alert("Please paste a valid video URL!");
      return;
    }

    const btn = document.getElementById('parseBtn');
    const parseStatus = document.getElementById('parseStatus');
    const resultBox = document.getElementById('downloadResult');

    // UI Loading state
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Parsing...';
    resultBox.style.display = 'none';
    parseStatus.style.display = 'block';
    parseStatus.innerHTML = '<div class="spinner"></div><p>Extracting media links from third-party API...</p>';

    // Mock API fetch delay for parsing
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = 'Parse Link';
      parseStatus.style.display = 'none';
      
      // Update UI with mock download details
      document.getElementById('dl-thumb').src = 'https://picsum.photos/seed/parse/160/90';
      document.getElementById('dl-title').innerText = "Extracted Video Content.mp4";
      document.getElementById('dl-meta').innerText = "Resolution: 1080p | Size: ~45 MB";
      
      // Note: Replace the href below with the actual JSON response direct link from your API
      document.getElementById('dl-link').href = "https://example.com/mock-download-link.mp4";
      
      resultBox.style.display = 'flex';
    }, 1500);
  }
</script>
