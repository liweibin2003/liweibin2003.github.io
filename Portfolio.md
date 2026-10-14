---
title: Photography Portfolio
subtitle: A collection of moments, seen through my lens.
layout: "page"
icon: fa-camera
order: 3
---

<!-- 引入 Fancybox 的 CSS 和 JS (用于点击放大和视频弹窗) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css" />
<script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js"></script>

<style>
/* 四宫格视频布局 */
.video-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2列 = 四宫格 */
  gap: 20px;
  margin-bottom: 50px;
  margin-top: 20px;
}
.video-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.video-item a {
  width: 100%;
  display: block;
}
.video-item video {
  width: 100%;
  aspect-ratio: 16 / 9; /* 统一视频封面比例 */
  object-fit: cover;
  border-radius: 8px; /* 略微圆角更好看 */
  cursor: pointer;
  background-color: #000;
  transition: opacity 0.3s ease;
}
.video-item video:hover {
  opacity: 0.85; /* 鼠标悬浮反馈 */
}
.video-title {
  font-size: 0.85em;
  color: #666;
  margin-top: 8px;
  font-weight: 500;
}

/* 九宫格图片布局 */
.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3列 = 九宫格 */
  gap: 15px;
}
.image-grid a {
  display: block;
  overflow: hidden;
  border-radius: 8px;
}
.image-grid img {
  width: 100%;
  aspect-ratio: 1 / 1; /* 强制正方形裁切，保证九宫格对齐 */
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s ease;
}
.image-grid img:hover {
  transform: scale(1.05); /* 鼠标悬浮图片微微放大 */
}
</style>

### Featured Videos
<!-- 视频四宫格区 -->
<div class="video-grid">
  <div class="video-item">
    <a href="{{ '/assets/images/1.mp4' | relative_url }}" data-fancybox="video-gallery">
      <video src="{{ '/assets/images/1.mp4' | relative_url }}" preload="metadata" muted></video>
    </a>
    <div class="video-title">视频 1 的标题</div>
  </div>
  <div class="video-item">
    <a href="{{ '/assets/images/2.mp4' | relative_url }}" data-fancybox="video-gallery">
      <video src="{{ '/assets/images/2.mp4' | relative_url }}" preload="metadata" muted></video>
    </a>
    <div class="video-title">视频 2 的标题</div>
  </div>
  <div class="video-item">
    <a href="{{ '/assets/images/3.mp4' | relative_url }}" data-fancybox="video-gallery">
      <video src="{{ '/assets/images/3.mp4' | relative_url }}" preload="metadata" muted></video>
    </a>
    <div class="video-title">视频 3 的标题</div>
  </div>
  <div class="video-item">
    <a href="{{ '/assets/images/4.mp4' | relative_url }}" data-fancybox="video-gallery">
      <video src="{{ '/assets/images/4.mp4' | relative_url }}" preload="metadata" muted></video>
    </a>
    <div class="video-title">视频 4 的标题</div>
  </div>
</div>

### Photo Gallery
<!-- 图片九宫格区 -->
<div class="image-grid">
  <a href="{{ '/assets/images/3.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/3.jpg' | relative_url }}" alt="Portfolio Image 3">
  </a>
  <a href="{{ '/assets/images/4.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/4.jpg' | relative_url }}" alt="Portfolio Image 4">
  </a>
  <a href="{{ '/assets/images/5.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/5.jpg' | relative_url }}" alt="Portfolio Image 5">
  </a>
  <a href="{{ '/assets/images/6.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/6.jpg' | relative_url }}" alt="Portfolio Image 6">
  </a>
  <a href="{{ '/assets/images/7.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/7.jpg' | relative_url }}" alt="Portfolio Image 7">
  </a>
  <a href="{{ '/assets/images/8.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/8.jpg' | relative_url }}" alt="Portfolio Image 8">
  </a>
  <a href="{{ '/assets/images/9.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/9.jpg' | relative_url }}" alt="Portfolio Image 9">
  </a>
  <!-- 注意：这里目前是7张图。因为采用的是CSS Grid，它会自动排布成3x3的网格，最后一行会空出两个位置。如果你想凑齐完美的九宫格，可以在文件夹中补充 10.jpg 和 11.jpg，并在此处复制添加两个 <a> 标签即可。 -->
</div>

<!-- 初始化 Fancybox 脚本 -->
<script>
  document.addEventListener("DOMContentLoaded", function() {
    Fancybox.bind('[data-fancybox]', {
      // 启用原图缩放和沉浸式体验
      Toolbar: {
        display: [
          "zoom",
          "slideShow",
          "fullscreen",
          "download",
          "close",
        ],
      },
    });
  });
</script>
