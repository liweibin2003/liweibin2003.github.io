---
title: Photography Portfolio
subtitle: A collection of moments, seen through my lens.
layout: "page"
icon: fa-camera
order: 2
---

<!-- 引入 Fancybox 的 CSS 和 JS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css" />
<script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js"></script>

<style>
/* === 这里是你原有的其他 CSS === */
/* 四宫格视频布局 */
.video-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); 
  /* ... 省略中间代码 ... */
}

.image-grid img:hover {
  transform: scale(1.05); /* 鼠标悬浮图片微微放大 */
}

.section-title {
  font-size: 1.5em;
  font-weight: bold;
  margin-top: 40px;
  margin-bottom: 20px;
  color: #333;
}

/* === 修复原主题 CSS 与 Fancybox 冲突导致大图不显示的问题 === */
.fancybox__container {
  z-index: 99999 !important; /* 确保弹窗图层在网页的最顶层 */
}

.fancybox__container img,
.fancybox__container .f-image {
  opacity: 1 !important;           /* 强制取消透明，解决懒加载冲突 */
  visibility: visible !important;  /* 强制可见 */
  display: block !important;       /* 覆盖可能的 display: none */
  animation: none !important;      /* 取消主题自带的图片载入动画 */
  box-shadow: none !important;     /* 去除多余阴影 */
  background: transparent !important;
}
</style>

<div class="section-title">Featured Videos</div>

<!-- ... 下面的 HTML 代码保持不变 ... -->

<!-- 视频四宫格区 -->
<div class="video-grid">
  <!-- 视频 1：YouTube 源 + 本地图片封面 -->
  <div class="video-item">
    <a href="https://youtu.be/In06Ry0ezLU" data-fancybox="video-gallery">
      <img src="{{ '/assets/images/3.jpg' | relative_url }}" alt="Video 1 Cover">
    </a>
    <div class="video-title">Mikumikudance</div>
  </div>

  <!-- 视频 2：YouTube 源 + 本地图片封面 -->
  <div class="video-item">
    <a href="https://youtu.be/iLsmqV9zqbU" data-fancybox="video-gallery">
      <img src="{{ '/assets/images/4.jpg' | relative_url }}" alt="Video 2 Cover">
    </a>
    <div class="video-title">CaltonHills-Drone</div>
  </div>

  <!-- 视频 3：本地 mp4 源 + 本地视频默认封面 -->
  <div class="video-item">
    <a href="{{ '/assets/images/3.mp4' | relative_url }}" data-fancybox="video-gallery">
      <video src="{{ '/assets/images/3.mp4' | relative_url }}" preload="metadata" muted></video>
    </a>
    <div class="video-title">Photoshop Tutorial: Cosplay</div>
  </div>

  <!-- 视频 4：本地 mp4 源 + 本地视频默认封面 -->
  <div class="video-item">
    <a href="{{ '/assets/images/4.mp4' | relative_url }}" data-fancybox="video-gallery">
      <video src="{{ '/assets/images/4.mp4' | relative_url }}" preload="metadata" muted></video>
    </a>
    <div class="video-title">Chinese Traditional Zither (me)</div>
  </div>
</div> <!-- 补上了这里缺失的关闭标签 -->

<div class="section-title">Photo Gallery</div>

<!-- 图片九宫格区 -->
<div class="image-grid">
  <a href="{{ '/assets/images/7.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/7.jpg' | relative_url }}" alt="Portfolio Image 7">
  </a>
  <a href="{{ '/assets/images/8.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/8.jpg' | relative_url }}" alt="Portfolio Image 8">
  </a>
  <a href="{{ '/assets/images/9.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/9.jpg' | relative_url }}" alt="Portfolio Image 9">
  </a>
  <a href="{{ '/assets/images/10.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/10.jpg' | relative_url }}" alt="Portfolio Image 10">
  </a>
  <a href="{{ '/assets/images/11.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/11.jpg' | relative_url }}" alt="Portfolio Image 11">
  </a>
  <a href="{{ '/assets/images/12.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/12.jpg' | relative_url }}" alt="Portfolio Image 12">
  </a>
  <a href="{{ '/assets/images/13.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/13.jpg' | relative_url }}" alt="Portfolio Image 13">
  </a>
  <a href="{{ '/assets/images/14.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/14.jpg' | relative_url }}" alt="Portfolio Image 14">
  </a>
  <a href="{{ '/assets/images/15.jpg' | relative_url }}" data-fancybox="image-gallery">
    <img src="{{ '/assets/images/15.jpg' | relative_url }}" alt="Portfolio Image 15">
  </a>
</div>

<!-- 初始化 Fancybox 脚本 -->
<script>
  document.addEventListener("DOMContentLoaded", function() {
    Fancybox.bind('[data-fancybox]', {
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
