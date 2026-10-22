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
  
  /* Platform Tabs */
  .crawler-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 24px;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
  }
  .tab-btn {
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    border: 1px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    background: #f5f5f5 !important;
    color: #333 !important; /* Fixed the invisible text issue */
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  /* Active states for different platforms */
  .tab-btn.active-yt { background: #FF0000 !important; color: #FFF !important; border-color: #FF0000; }
  .tab-btn.active-tw { background: #9146FF !important; color: #FFF !important; border-color: #9146FF; }
  .tab-btn.active-vi { background: #1AB7EA !important; color: #FFF !important; border-color: #1AB7EA; }
  .tab-btn.active-dm { background: #0066DC !important; color: #FFF !important; border-color: #0066DC; }

  /* Search Area */
  .search-container {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
  }
  .search-input {
    flex: 1;
    padding: 12px 16px;
    font-size: 16px;
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
    font-size: 16px;
    font-weight: bold;
    color: #fff;
    background: #333;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s;
  }
  .search-btn:hover { background: #000; }
  .search-btn:disabled { background: #ccc; cursor: not-allowed; }

  /* Dynamic Filter Panel */
  .filter-panel {
    display: none;
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 24px;
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
    padding: 40px 0;
    color: #888;
    font-size: 15px;
  }
  .spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #333;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px auto;
  }
  @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

  /* Results Grid */
  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  .video-card {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border: 1px solid #f0f0f0;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .video-card:hover { 
    transform: translateY(-4px); 
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
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
    font-size: 15px;
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
    font-size: 13px;
    color: #666;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .meta-highlight {
    font-weight: bold;
    color: #222;
  }
</style>

<div class="crawler-app">
  
  <!-- 1. Platform Tabs -->
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

  <!-- 2. Main Search Box -->
  <div class="search-container">
    <input type="text" id="searchInput" class="search-input" placeholder="Enter keyword, e.g., Speedrun, Game Trailer...">
    <button id="searchBtn" class="search-btn" onclick="fetchData()">Fetch Data</button>
  </div>

  <!-- 3. YouTube Filters -->
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

  <!-- 4. Twitch Filters -->
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

  <!-- 5. Vimeo Filters -->
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
    <div class="filter-group">
      <label>License</label>
      <select id="vi-license">
        <option value="any">Any License</option>
        <option value="cc">Creative Commons</option>
      </select>
    </div>
  </div>

  <!-- 6. Dailymotion Filters -->
  <div id="filters-dailymotion" class="filter-panel">
    <div class="filter-group">
      <label>Sort By</label>
      <select id="dm-sort">
        <option value="relevance">Relevance</option>
        <option value="visited">Most Viewed</option>
        <option value="recent">Most Recent</option>
      </select>
    </div>
    <div class="filter-group">
      <label>Resolution</label>
      <select id="dm-quality">
        <option value="all">Any Quality</option>
        <option value="hd">HD / 4K Only</option>
      </select>
    </div>
  </div>

  <!-- 7. Status & Results Area -->
  <div id="statusArea" class="status-area">
    Waiting for search input...
  </div>
  
  <div id="resultsGrid" class="results-grid"></div>

</div>

<script>
  let currentPlatform = 'youtube';

  // Logic for switching platforms
  function switchPlatform(platform) {
    currentPlatform = platform;
    
    // Reset all buttons to default class
    document.getElementById('tab-yt').className = 'tab-btn';
    document.getElementById('tab-tw').className = 'tab-btn';
    document.getElementById('tab-vi').className = 'tab-btn';
    document.getElementById('tab-dm').className = 'tab-btn';

    // Apply active class to selected button
    if (platform === 'youtube') document.getElementById('tab-yt').classList.add('active-yt');
    if (platform === 'twitch') document.getElementById('tab-tw').classList.add('active-tw');
    if (platform === 'vimeo') document.getElementById('tab-vi').classList.add('active-vi');
    if (platform === 'dailymotion') document.getElementById('tab-dm').classList.add('active-dm');
    
    // Hide all filter panels
    document.getElementById('filters-youtube').classList.remove('active');
    document.getElementById('filters-twitch').classList.remove('active');
    document.getElementById('filters-vimeo').classList.remove('active');
    document.getElementById('filters-dailymotion').classList.remove('active');

    // Show active filter panel
    document.getElementById(`filters-${platform}`).classList.add('active');
    
    // Clear results area
    document.getElementById('resultsGrid').innerHTML = '';
    document.getElementById('statusArea').style.display = 'block';
    document.getElementById('statusArea').innerHTML = 'Waiting for search input...';
  }

  // Trigger data fetch
  async function fetchData() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) {
      alert("Please enter a search keyword first!");
      return;
    }

    // Set UI to loading state
    const btn = document.getElementById('searchBtn');
    const statusArea = document.getElementById('statusArea');
    const resultsGrid = document.getElementById('resultsGrid');
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Fetching...';
    statusArea.style.display = 'block';
    statusArea.innerHTML = '<div class="spinner"></div><p>Fetching data via Serverless API...</p>';
    resultsGrid.innerHTML = '';

    // Simulate network delay (1.5 seconds)
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = 'Fetch Data';
      statusArea.style.display = 'none';
      
      const mockData = generateMockData(currentPlatform, query);
      renderResults(mockData, currentPlatform);
    }, 1500);
  }

  // Render cards based on platform
  function renderResults(data, platform) {
    const grid = document.getElementById('resultsGrid');
    
    if (data.length === 0) {
      document.getElementById('statusArea').style.display = 'block';
      document.getElementById('statusArea').innerHTML = 'No results found.';
      return;
    }

    data.forEach(item => {
      const card = document.createElement('div');
      card.className = 'video-card';
      
      let cardInnerHTML = `<img class="video-cover" src="${item.thumbnail}" alt="cover"><div class="video-info">`;

      if (platform === 'youtube') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta">
              <span><i class="fa-solid fa-user"></i> ${item.channel}</span>
              <span>${item.date}</span>
            </div>
            <div class="video-meta meta-highlight">
              <span><i class="fa-solid fa-eye"></i> ${item.views} Views</span>
              <span><i class="fa-solid fa-thumbs-up"></i> ${item.likes}</span>
            </div>
        `;
      } else if (platform === 'twitch') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta">
              <span><i class="fa-solid fa-user"></i> ${item.streamer}</span>
              <span>${item.duration}</span>
            </div>
            <div class="video-meta meta-highlight">
              <span style="color: #9146FF"><i class="fa-solid fa-gamepad"></i> ${item.category}</span>
              <span><i class="fa-solid fa-users"></i> ${item.viewers}</span>
            </div>
        `;
      } else if (platform === 'vimeo') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta">
              <span><i class="fa-solid fa-user"></i> ${item.creator}</span>
              <span>${item.duration}</span>
            </div>
            <div class="video-meta meta-highlight">
              <span style="color: #1AB7EA"><i class="fa-solid fa-play"></i> ${item.plays} Plays</span>
              <span><i class="fa-solid fa-heart"></i> ${item.likes}</span>
            </div>
        `;
      } else if (platform === 'dailymotion') {
        cardInnerHTML += `
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta">
              <span><i class="fa-solid fa-user"></i> ${item.owner}</span>
              <span>${item.date}</span>
            </div>
            <div class="video-meta meta-highlight">
              <span style="color: #0066DC"><i class="fa-solid fa-eye"></i> ${item.views} Views</span>
              <span><i class="fa-solid fa-clock"></i> ${item.duration}</span>
            </div>
        `;
      }

      cardInnerHTML += `</div>`;
      card.innerHTML = cardInnerHTML;
      grid.appendChild(card);
    });
  }

  // Generate mock data for UI testing
  function generateMockData(platform, query) {
    return [1, 2, 3, 4, 5, 6].map(i => {
      if (platform === 'youtube') {
        return {
          title: `[${query}] Episode ${i}: Deep Dive & Gameplay`,
          channel: "Gamer HQ",
          views: (Math.random() * 10 + 1).toFixed(1) + "M",
          likes: Math.floor(Math.random() * 50000) + 1000,
          date: "Oct 1" + i + ", 2024",
          thumbnail: `https://picsum.photos/seed/${query}yt${i}/400/225`
        };
      } else if (platform === 'twitch') {
        return {
          title: `${query} World Record Attempt #${i}`,
          streamer: "SpeedDemon_" + i,
          category: query,
          viewers: Math.floor(Math.random() * 20000) + 500,
          duration: "02:14:05",
          thumbnail: `https://picsum.photos/seed/${query}tw${i}/400/225`
        };
      } else if (platform === 'vimeo') {
        return {
          title: `${query} - Official Cinematic Trailer ${i}`,
          creator: "Creative Studio " + i,
          plays: Math.floor(Math.random() * 900) + 100 + "K",
          likes: Math.floor(Math.random() * 8000) + 500,
          duration: "03:45",
          thumbnail: `https://picsum.photos/seed/${query}vi${i}/400/225`
        };
      } else {
        return {
          title: `How to master ${query} | Tutorial Part ${i}`,
          owner: "DailyGamer" + i,
          views: Math.floor(Math.random() * 500) + 10 + "K",
          date: i + " days ago",
          duration: "12:30",
          thumbnail: `https://picsum.photos/seed/${query}dm${i}/400/225`
        };
      }
    });
  }
</script>
