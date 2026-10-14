---
title: Cool Websites
subtitle: Interesting websites worth checking out.
layout: "page"
icon: fa-globe
order: 3
---

<style>
/* 网站列表整体布局 */
.website-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
}

/* 单个网站卡片样式 */
.website-card {
  padding: 1.5rem;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  background-color: #ffffff;
  transition: box-shadow 0.3s ease, transform 0.2s ease;
}

.website-card:hover {
  box-shadow: 0 8px 24px rgba(149, 157, 165, 0.2);
  transform: translateY(-2px);
}

/* 网址链接样式（带下划线） */
.website-link {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0366d6;
  text-decoration: underline;
  text-underline-offset: 4px; /* 让下划线稍微靠下，排版更透气 */
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.website-link:hover {
  color: #005cc5;
}

/* 外部链接小图标 */
.external-icon {
  font-size: 0.85em;
  text-decoration: none;
  display: inline-block;
}

/* 英文介绍文字样式 */
.website-desc {
  font-size: 1rem;
  color: #586069;
  margin-top: 0.8rem;
  line-height: 1.5;
}
</style>

<div class="website-list">

  <!-- xiaoce.fun -->
  <div class="website-card">
    <a href="https://xiaoce.fun" target="_blank" class="website-link">
      xiaoce.fun <span class="external-icon">↗</span>
    </a>
    <div class="website-desc">
      Put your knowledge to the test across various domains with a collection of fun and engaging mini-quizzes.
    </div>
  </div>

  <!-- jazzvswaffles.com -->
  <div class="website-card">
    <a href="https://jazzvswaffles.com" target="_blank" class="website-link">
      jazzvswaffles.com
