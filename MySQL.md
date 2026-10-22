---
title: MySQL
subtitle: Coming soon
layout: "page"
icon: fa-table
order: 4
---

---
title: MySQL
subtitle: 交互式 SQL 数据分析引擎
layout: "page"
icon: fa-table
order: 4
---

<style>
  /* 页面独立样式，避免污染原有博客主题 */
  .sql-showcase { font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; }
  .sql-header { margin-bottom: 2rem; padding: 1rem; background: #f8f9fa; border-left: 4px solid #3b82f6; border-radius: 4px; }
  .sql-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }
  @media (max-width: 768px) { .sql-layout { grid-template-columns: 1fr; } }
  .box-title { font-weight: 600; margin-bottom: 1rem; border-bottom: 2px solid #eee; padding-bottom: 0.5rem; }
  .preset-btn { display: block; width: 100%; text-align: left; padding: 0.75rem 1rem; margin-bottom: 0.75rem; background: #fff; border: 1px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 0.9rem; }
  .preset-btn:hover { border-color: #3b82f6; background: #eff6ff; color: #1d4ed8; }
  .preset-desc { font-size: 0.8rem; color: #666; margin-top: 0.25rem; }
  .editor-container { border: 1px solid #ddd; border-radius: 6px; overflow: hidden; margin-bottom: 1rem; }
  .CodeMirror { height: auto !important; min-height: 200px; font-family: 'Fira Code', monospace, consolas; font-size: 14px; }
  .action-bar { display: flex; gap: 1rem; margin-bottom: 1rem; align-items: center; }
  .btn-run { background: #10b981; color: white; border: none; padding: 0.5rem 1.5rem; border-radius: 4px; cursor: pointer; font-weight: bold; }
  .btn-run:hover { background: #059669; }
  .btn-clear { background: #f3f4f6; color: #374151; border: 1px solid #d1d5db; padding: 0.5rem 1.5rem; border-radius: 4px; cursor: pointer; }
  .btn-clear:hover { background: #e5e7eb; }
  .status-badge { font-size: 0.85rem; padding: 0.2rem 0.6rem; border-radius: 20px; background: #e0e7ff; color: #4338ca; display: none; }
  .result-area { overflow-x: auto; background: #fff; border: 1px solid #ddd; border-radius: 6px; min-height: 100px; padding: 1rem; }
  .result-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left; }
  .result-table th, .result-table td { padding: 0.75rem; border-bottom: 1px solid #eee; }
  .result-table th { background: #f9fafb; font-weight: 600; white-space: nowrap; }
  .error-msg { color: #dc2626; font-family: monospace; white-space: pre-wrap; }
  .sql-footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px dashed #ccc; font-size: 0.85rem; color: #666; }
</style>

<!-- 依赖库引入 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/dracula.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/sql/sql.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.js"></script>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'default' });
</script>

<div class="sql-showcase">
  
  <div class="sql-header">
    <strong>极客声明：</strong>本页面不依赖任何后端服务器。底层的 SQL 引擎完全通过 WebAssembly (sql.js) 在你的浏览器内存中实时运行。为了兼容浏览器环境，底层采用 SQLite，但完美兼容 MySQL 的核心 DML 查询、多表 JOIN 与窗口函数。
  </div>

  <div class="sql-layout">
    <!-- 左侧：数据库架构 -->
    <div>
      <div class="box-title">📊 业务线 ER 图 (Schema)</div>
      <div class="mermaid">
        erDiagram
            USERS ||--o{ ORDERS : places
            PRODUCTS ||--o{ ORDER_ITEMS : contains
            ORDERS ||--|{ ORDER_ITEMS : includes
            USERS {
                int user_id PK
                date register_date
                varchar user_tier "Bronze, Silver, Gold, Platinum"
            }
            PRODUCTS {
                int product_id PK
                varchar category
                decimal price
                decimal cost
            }
            ORDERS {
                int order_id PK
                int user_id FK
                date order_date
                varchar status "Completed, Pending, Cancelled"
            }
            ORDER_ITEMS {
                int order_id FK
                int product_id FK
                int quantity
            }
      </div>
    </div>

    <!-- 右侧：预设查询剧本 -->
    <div>
      <div class="box-title">💡 预设分析剧本 (点击填充 SQL)</div>
      
      <button class="preset-btn" onclick="loadPreset(1)">
        <strong>1. 复杂多表关联与聚合</strong>
        <div class="preset-desc">计算各商品品类的利润贡献度 (关联订单、明细、商品三张表)</div>
      </button>

      <button class="preset-btn" onclick="loadPreset(2)">
        <strong>2. 高级窗口函数 (Window Functions)</strong>
        <div class="preset-desc">使用 RANK() 找出每个月消费金额 TOP 3 的超级用户</div>
      </button>

      <button class="preset-btn" onclick="loadPreset(3)">
        <strong>3. CTE 公用表表达式应用</strong>
        <div class="preset-desc">使用 WITH 和 LAG() 函数，计算高价值用户的平均复购周期</div>
      </button>
    </div>
  </div>

  <!-- 下方：交互式查询台 -->
  <div class="box-title">💻 SQL Playground</div>
  <div class="editor-container">
    <textarea id="sql-editor"></textarea>
  </div>
  
  <div class="action-bar">
    <button class="btn-run" onclick="executeSQL()" id="run-btn">🚀 正在加载引擎...</button>
    <button class="btn-clear" onclick="clearEditor()">清空</button>
    <span class="status-badge" id="exec-time"></span>
  </div>

  <div class="result-area" id="result-container">
    <div style="color: #666; text-align: center; margin-top: 1rem;">查询结果将显示在这里...</div>
  </div>

  <div class="sql-footer">
    <p>
      * 声明：本页面使用的数据完全由 Python 脚本基于随机数与预设概率生成，不涉及任何真实的商业数据。
      <br>
      📥 你可以下载我编写的数据生成脚本自己跑一遍：<a href="/assets/generate_db.py" target="_blank">assets/generate_db.py</a>
      <br>
      📦 或者直接下载本页面正在使用的 SQLite 数据库文件：<a href="/assets/database.sqlite" target="_blank">assets/database.sqlite</a>
    </p>
  </div>

</div>

<script>
  // 预设 SQL 剧本库
  const presets = {
    1: `-- 查询各品类利润贡献度 (过滤已完成订单)
SELECT 
    p.category AS '商品品类',
    ROUND(SUM((p.price - p.cost) * oi.quantity), 2) AS '总利润',
    COUNT(DISTINCT o.order_id) AS '订单数量'
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY 总利润 DESC;`,

    2: `-- 找出每个月消费金额 TOP 3 的用户
WITH MonthlySpending AS (
    SELECT 
        strftime('%Y-%m', o.order_date) AS month,
        u.user_id,
        u.user_tier,
        SUM(p.price * oi.quantity) AS total_spent
    FROM orders o
    JOIN users u ON o.user_id = u.user_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
    GROUP BY month, u.user_id
),
RankedSpending AS (
    SELECT 
        month AS '月份',
        user_id AS '用户ID',
        user_tier AS '会员等级',
        ROUND(total_spent, 2) AS '月消费总额',
        RANK() OVER(PARTITION BY month ORDER BY total_spent DESC) as rank
    FROM MonthlySpending
)
SELECT * FROM RankedSpending 
WHERE rank <= 3 
ORDER BY 月份 DESC, rank ASC;`,

    3: `-- 查询高价值用户的平均复购周期 (相连两次订单的间隔天数)
WITH UserOrders AS (
    SELECT 
        user_id,
        order_date,
        LAG(order_date) OVER(PARTITION BY user_id ORDER BY order_date) as prev_order_date
    FROM orders
    WHERE status = 'Completed'
)
SELECT 
    u.user_id AS '用户ID',
    u.user_tier AS '会员等级',
    COUNT(uo.order_date) AS '总订单数',
    ROUND(AVG(julianday(uo.order_date) - julianday(uo.prev_order_date)), 1) AS '平均复购周期(天)'
FROM UserOrders uo
JOIN users u ON uo.user_id = u.user_id
WHERE uo.prev_order_date IS NOT NULL
GROUP BY u.user_id
HAVING 总订单数 >= 3
ORDER BY [平均复购周期(天)] ASC
LIMIT 10;`
  };

  let db = null;
  let editor = null;

  // 初始化 CodeMirror 编辑器
  document.addEventListener("DOMContentLoaded", () => {
    editor = CodeMirror.fromTextArea(document.getElementById('sql-editor'), {
      mode: 'text/x-sql',
      theme: 'dracula',
      lineNumbers: true,
      lineWrapping: true,
      viewportMargin: Infinity
    });
    editor.setValue("-- 在这里编写你的 SQL，或者点击上方预设按钮\nSELECT * FROM users LIMIT 5;");
    
    // 初始化 WebAssembly SQL 引擎并拉取数据
    initDatabase();
  });

  async function initDatabase() {
    const runBtn = document.getElementById('run-btn');
    try {
      // 加载 sql.js
      const sqlPromise = initSqlJs({
        locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
      });
      // 并发请求数据库文件，确保放在 /assets/ 目录下
      const dataPromise = fetch('/assets/database.sqlite').then(res => {
        if (!res.ok) throw new Error("无法加载 database.sqlite，请检查文件是否上传并排除了 Jekyll 过滤。");
        return res.arrayBuffer();
      });

      const [SQL, buf] = await Promise.all([sqlPromise, dataPromise]);
      db = new SQL.Database(new Uint8Array(buf));
      
      runBtn.innerText = "🚀 运行 SQL (Run)";
      runBtn.disabled = false;
    } catch (err) {
      runBtn.innerText = "引擎加载失败";
      runBtn.style.background = "#ef4444";
      document.getElementById('result-container').innerHTML = `<div class="error-msg">初始化错误: ${err.message}</div>`;
    }
  }

  function loadPreset(id) {
    if(editor) {
      editor.setValue(presets[id]);
      // 给一点延迟让视觉上有反馈，然后自动执行
      setTimeout(executeSQL, 100);
    }
  }

  function clearEditor() {
    if(editor) editor.setValue("");
    document.getElementById('result-container').innerHTML = `<div style="color: #666; text-align: center; margin-top: 1rem;">查询结果将显示在这里...</div>`;
    document.getElementById('exec-time').style.display = 'none';
  }

  function executeSQL() {
    if (!db || !editor) return;
    
    const query = editor.getValue().trim();
    if (!query) return;

    const resultContainer = document.getElementById('result-container');
    const timeBadge = document.getElementById('exec-time');
    
    try {
      const start = performance.now();
      const results = db.exec(query);
      const end = performance.now();
      
      timeBadge.innerText = `⏱️ 耗时: ${(end - start).toFixed(1)} ms`;
      timeBadge.style.display = 'inline-block';

      if (results.length === 0) {
        resultContainer.innerHTML = '<div style="color: #10b981; margin-top: 1rem;">✅ 成功执行，无数据返回 (0 rows)。</div>';
        return;
      }

      // 渲染表格
      let html = '<table class="result-table"><thead><tr>';
      const columns = results[0].columns;
      const values = results[0].values;

      columns.forEach(col => { html += `<th>${col}</th>`; });
      html += '</tr></thead><tbody>';

      values.forEach(row => {
        html += '<tr>';
        row.forEach(val => { 
          // 处理 NULL 和数字格式
          let displayVal = val === null ? '<em>NULL</em>' : val;
          html += `<td>${displayVal}</td>`; 
        });
        html += '</tr>';
      });
      html += '</tbody></table>';

      resultContainer.innerHTML = html;

    } catch (err) {
      timeBadge.style.display = 'none';
      resultContainer.innerHTML = `<div class="error-msg">SQL 语法错误:\n${err.message}</div>`;
    }
  }
</script>
