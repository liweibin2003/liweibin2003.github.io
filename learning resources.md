---
title: Learning Resources
subtitle: Curated tutorials, tools, and resources to help you learn and build.
layout: "page"
icon: fa-book
order: 4
---

<style>
/* 资源列表整体布局 */
.resource-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
}

/* 单个资源卡片样式 */
.resource-card {
  padding: 1.5rem;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  background-color: #ffffff;
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  text-decoration: none;
  color: inherit;
  display: block;
}

.resource-card:hover {
  box-shadow: 0 8px 24px rgba(149, 157, 165, 0.2);
  transform: translateY(-2px);
}

/* 标题样式 */
.resource-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #24292e;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

/* 专门针对要求下划线的标题 */
.highlight-link {
  text-decoration: underline;
  text-underline-offset: 4px;
  color: #0366d6;
}

/* 底部元数据（作者、标签） */
.resource-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.9rem;
  color: #586069;
}

/* 分类标签样式 */
.badge {
  padding: 0.2em 0.8em;
  border-radius: 2em;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.badge-video {
  background-color: #f1f8ff;
  color: #0366d6;
  border: 1px solid #c8e1ff;
}
.badge-book {
  background-color: #fcf1f4;
  color: #cb2431;
  border: 1px solid #f9cacc;
}
.badge-original {
  background-color: #e6ffed;
  color: #22863a;
  border: 1px solid #b1f0c2;
}

/* 作者图标 (可选) */
.author-icon {
  margin-right: 4px;
}
</style>

<div class="resource-list">

  <!-- Resource 1 -->
  <a href="https://www.bilibili.com/video/BV1E4411B7ef" target="_blank" class="resource-card">
    <div class="resource-title">Tableau for Beginners: Zero to Hero Tutorial</div>
    <div class="resource-meta">
      <span class="badge badge-video">Video</span>
      <span><i class="author-icon">✍️</i> Author: 未明学院</span>
    </div>
  </a>

  <!-- Resource 2 -->
  <a href="https://www.bilibili.com/video/BV1Jgf6YvE8e" target="_blank" class="resource-card">
    <div class="resource-title">Python Quick Start Tutorial</div>
    <div class="resource-meta">
      <span class="badge badge-video">Video</span>
      <span><i class="author-icon">✍️</i> Author: 林粒粒呀</span>
    </div>
  </a>

  <!-- Resource 3 (带有下划线链接的原创内容) -->
  <a href="https://www.bilibili.com/video/BV1YafYYTEVW" target="_blank" class="resource-card">
    <div class="resource-title highlight-link">How to Create High-Quality Background Composites for Cosplay Photos using Photoshop</div>
    <div class="resource-meta">
      <span class="badge badge-original">Original Tutorial</span>
      <span><i class="author-icon">✍️</i> Author: 本人</span>
    </div>
  </a>

  <!-- Resource 4 -->
  <a href="https://www.bilibili.com/video/BV1gX8R6nEN2" target="_blank" class="resource-card">
    <div class="resource-title">Creating MMD Animations in Blender 3D (Without MikuMikuDance)</div>
    <div class="resource-meta">
      <span class="badge badge-video">Video</span>
      <span><i class="author-icon">✍️</i> Author: 知知呜Blender</span>
    </div>
  </a>

  <!-- Resource 5 -->
  <a href="https://www.txtduo.com/html/71381/" target="_blank" class="resource-card">
    <div class="resource-title">[eBook] The Three-Body Problem - China's Best Sci-Fi Novel</div>
    <div class="resource-meta">
      <span class="badge badge-book">eBook</span>
      <span><i class="author-icon">✍️</i> Author: 刘慈欣</span>
    </div>
  </a>

</div>
