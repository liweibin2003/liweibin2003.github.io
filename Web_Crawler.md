---
title: Web Crawler
subtitle: Coming soon
layout: "page"
icon: fa-bug
order: 5
---

<!-- 引入 Font Awesome (如果你的 Jekyll 主题已包含可忽略) -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
  /* 独立作用域，防止污染全局 Jekyll 样式 */
  .crawler-app {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    max-width: 1000px;
    margin: 0 auto;
    color: #333;
  }
  
  /* 平台切换 Tab */
  .crawler-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 24px;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
  }
  .tab-btn {
    padding: 10px 24px;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    background: #f5f5f5;
    color: #666;
    transition: all 0.3s ease;
  }
  .tab-btn i { margin-right: 8px; }
  .tab-btn.active-yt { background: #ff0000; color: #fff; }
  .tab-btn.active-tw { background: #9146FF; color: #fff; }

  /* 搜索区域 */
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
  }
  .search-input:focus { border-color: #333; }
  .search-btn {
    padding: 0 24px;
    font-size: 16px;
    font-weight: bold;
    color: white;
    background: #333;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s;
  }
  .search-btn:hover { background: #000; }
  .search-btn:disabled { background: #ccc; cursor: not-allowed; }

  /* 动态筛选面板 */
  .filter-panel {
    display: none;
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 24px;
    gap: 16px;
    flex-wrap: wrap;
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
  }

  /* 状态展示区 */
  .status-area {
    text-align: center;
    padding: 40px 0;
    color: #888;
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

  /* 视频结果网格 */
  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  .video-card {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s;
  }
  .video-card:hover { transform: translateY(-4px); }
  .video-cover {
    width: 100%;
    aspect-ratio: 16/9;
    background: #e0e0e0;
    object-fit: cover;
  }
  .video-info { padding: 16px; }
  .video-title {
    font-size: 16px;
    font-weight: bold;
    margin: 0 0 8px 0;
    line-height: 1.4;
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
    margin-bottom: 6px;
  }
  .meta-highlight {
    font-weight: bold;
    color: #333;
  }
</style>

<div class="crawler-app">
  
  <!-- 1. 平台切换 -->
  <div class="crawler-tabs">
    <button class="tab-btn active-yt" onclick="switchPlatform('youtube')" id="tab-yt">
      <i class="fa-brands fa-youtube"></i> YouTube
    </button>
    <button class="tab-btn" onclick="switchPlatform('twitch')" id="tab-tw">
      <i class="fa-brands fa-twitch"></i> Twitch
    </button>
  </div>

  <!-- 2. 核心搜索框 -->
  <div class="search-container">
    <input type="text" id="searchInput" class="search-input" placeholder="输入关键词，例如：黑神话悟空...">
    <button id="searchBtn" class="search-btn" onclick="fetchData()">获取数据</button>
  </div>

  <!-- 3. YouTube 专属筛选器 -->
  <div id="filters-youtube" class="filter-panel active">
    <div class="filter-group">
      <label>排序方式 (Order)</label>
      <select id="yt-order">
        <option value="viewCount">播放量最高</option>
        <option value="date">最新发布</option>
        <option value="relevance">相关度</option>
      </select>
    </div>
    <div class="filter-group">
      <label>视频时长 (Duration)</label>
      <select id="yt-duration">
        <option value="any">不限时</option>
        <option value="short">短视频 (<4分钟)</option>
        <option value="long">长视频 (>20分钟)</option>
      </select>
    </div>
  </div>

  <!-- 4. Twitch 专属筛选器 -->
  <div id="filters-twitch" class="filter-panel">
    <div class="filter-group">
      <label>内容类型 (Type)</label>
      <select id="tw-type">
        <option value="streams">正在直播 (Live)</option>
        <option value="vods">完整录播 (VODs)</option>
        <option value="clips">高光切片 (Clips)</option>
      </select>
    </div>
    <div class="filter-group">
      <label>排序 (Sort)</label>
      <select id="tw-sort">
        <option value="views">观看人数/播放量</option>
        <option value="trending">当前热门</option>
      </select>
    </div>
  </div>

  <!-- 5. 状态反馈与结果展示 -->
  <div id="statusArea" class="status-area">
    等待输入搜索条件...
  </div>
  
  <div id="resultsGrid" class="results-grid"></div>

</div>

<script>
  let currentPlatform = 'youtube';

  // 切换平台 UI 逻辑
  function switchPlatform(platform) {
    currentPlatform = platform;
    
    // 按钮样式切换
    document.getElementById('tab-yt').className = 'tab-btn ' + (platform === 'youtube' ? 'active-yt' : '');
    document.getElementById('tab-tw').className = 'tab-btn ' + (platform === 'twitch' ? 'active-tw' : '');
    
    // 筛选面板切换
    document.getElementById('filters-youtube').classList.toggle('active', platform === 'youtube');
    document.getElementById('filters-twitch').classList.toggle('active', platform === 'twitch');
    
    // 清空结果
    document.getElementById('resultsGrid').innerHTML = '';
    document.getElementById('statusArea').style.display = 'block';
    document.getElementById('statusArea').innerHTML = '等待输入搜索条件...';
  }

  // 触发搜索请求
  async function fetchData() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) {
      alert("请先输入搜索关键词！");
      return;
    }

    // UI 进入 Loading 状态
    const btn = document.getElementById('searchBtn');
    const statusArea = document.getElementById('statusArea');
    const resultsGrid = document.getElementById('resultsGrid');
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 抓取中...';
    statusArea.style.display = 'block';
    statusArea.innerHTML = '<div class="spinner"></div><p>正在通过 Serverless API 获取数据...</p>';
    resultsGrid.innerHTML = '';

    // TODO: 这里是未来对接云函数的地方
    // const params = currentPlatform === 'youtube' 
    //   ? `?q=${query}&order=${document.getElementById('yt-order').value}` 
    //   : `?q=${query}&type=${document.getElementById('tw-type').value}`;
    // const response = await fetch(`https://your-api.workers.dev/${currentPlatform}${params}`);
    // const data = await response.json();

    // 模拟网络延迟和伪造数据 (1.5秒后返回)
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = '获取数据';
      statusArea.style.display = 'none';
      
      const mockData = generateMockData(currentPlatform, query);
      renderResults(mockData, currentPlatform);
    }, 1500);
  }

  // 渲染卡片
  function renderResults(data, platform) {
    const grid = document.getElementById('resultsGrid');
    
    if (data.length === 0) {
      document.getElementById('statusArea').style.display = 'block';
      document.getElementById('statusArea').innerHTML = '没有找到相关视频。';
      return;
    }

    data.forEach(item => {
      const card = document.createElement('div');
      card.className = 'video-card';
      
      // 根据平台渲染不同的数据字段
      if (platform === 'youtube') {
        card.innerHTML = `
          <img class="video-cover" src="${item.thumbnail}" alt="cover">
          <div class="video-info">
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta">
              <span><i class="fa-solid fa-user"></i> ${item.channel}</span>
              <span>${item.date}</span>
            </div>
            <div class="video-meta meta-highlight">
              <span><i class="fa-solid fa-eye"></i> ${item.views}</span>
              <span><i class="fa-solid fa-thumbs-up"></i> ${item.likes}</span>
            </div>
          </div>
        `;
      } else {
        card.innerHTML = `
          <img class="video-cover" src="${item.thumbnail}" alt="cover">
          <div class="video-info">
            <h3 class="video-title">${item.title}</h3>
            <div class="video-meta">
              <span><i class="fa-solid fa-user"></i> ${item.streamer}</span>
              <span>${item.duration}</span>
            </div>
            <div class="video-meta meta-highlight">
              <span style="color: #9146FF"><i class="fa-solid fa-gamepad"></i> ${item.category}</span>
              <span><i class="fa-solid fa-users"></i> ${item.viewers} 在看</span>
            </div>
          </div>
        `;
      }
      grid.appendChild(card);
    });
  }

  // 生成用于前端预览的模拟数据 (Mock Data)
  function generateMockData(platform, query) {
    return [1, 2, 3, 4, 5, 6].map(i => {
      if (platform === 'youtube') {
        return {
          title: `【${query}】第 ${i} 期：深度解析与实战攻略`,
          channel: "硬核游戏局",
          views: (Math.random() * 100).toFixed(1) + "万",
          likes: Math.floor(Math.random() * 5000) + 100,
          date: "2024-03-1" + i,
          thumbnail: `https://picsum.photos/seed/${query}yt${i}/400/225`
        };
      } else {
        return {
          title: `${query} Speedrun Record Try #${i}`,
          streamer: "SpeedDemon" + i,
          category: query,
          viewers: Math.floor(Math.random() * 20000) + 500,
          duration: "02:14:05",
          thumbnail: `https://picsum.photos/seed/${query}tw${i}/400/225`
        };
      }
    });
  }
</script>
