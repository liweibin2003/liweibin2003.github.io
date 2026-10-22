---
title: MySQL
subtitle: Interactive SQL Data Analysis Engine
layout: "page"
icon: fa-table
order: 4
---

<style>
  .sql-showcase { font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; }
  .sql-header { margin-bottom: 2rem; padding: 1rem; background: #f8f9fa; border-left: 4px solid #3b82f6; border-radius: 4px; color: #374151; }
  .sql-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }
  @media (max-width: 768px) { .sql-layout { grid-template-columns: 1fr; } }
  .box-title { font-weight: 600; margin-bottom: 1rem; border-bottom: 2px solid #eee; padding-bottom: 0.5rem; color: #111827; }
  .preset-btn { display: block; width: 100%; text-align: left; padding: 0.75rem 1rem; margin-bottom: 0.75rem; background: #fff; border: 1px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 0.9rem; color: #111827; }
  .preset-btn:hover { border-color: #3b82f6; background: #eff6ff; color: #1d4ed8; }
  .preset-desc { font-size: 0.8rem; color: #666; margin-top: 0.25rem; }
  .editor-container { border: 1px solid #ddd; border-radius: 6px; overflow: hidden; margin-bottom: 1rem; }
  .CodeMirror { height: auto !important; min-height: 200px; font-family: 'Fira Code', monospace, consolas; font-size: 14px; text-align: left; }
  .action-bar { display: flex; gap: 1rem; margin-bottom: 1rem; align-items: center; }
  .btn-run { background: #10b981; color: white; border: none; padding: 0.5rem 1.5rem; border-radius: 4px; cursor: pointer; font-weight: bold; }
  .btn-run:hover { background: #059669; }
  .btn-clear { background: #f3f4f6; color: #374151; border: 1px solid #d1d5db; padding: 0.5rem 1.5rem; border-radius: 4px; cursor: pointer; }
  .btn-clear:hover { background: #e5e7eb; }
  .status-badge { font-size: 0.85rem; padding: 0.2rem 0.6rem; border-radius: 20px; background: #e0e7ff; color: #4338ca; display: none; }
  .result-area { overflow-x: auto; background: #fff; border: 1px solid #ddd; border-radius: 6px; min-height: 100px; padding: 1rem; }
  .result-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left; }
  /* Fixed White Text Issue */
  .result-table th, .result-table td { padding: 0.75rem; border-bottom: 1px solid #eee; color: #374151 !important; }
  .result-table th { background: #f9fafb; font-weight: 600; white-space: nowrap; color: #111827 !important; }
  .error-msg { color: #dc2626; font-family: monospace; white-space: pre-wrap; }
  .sql-footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px dashed #ccc; font-size: 0.85rem; color: #666; }
</style>

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
    <strong>Geek Statement:</strong> This page does not rely on any backend server. The underlying SQL engine runs in real-time entirely within your browser's memory via WebAssembly (sql.js). To ensure browser compatibility, SQLite is used under the hood, seamlessly supporting core MySQL DML queries, multi-table JOINs, and window functions.
  </div>

  <div class="sql-layout">
    <div>
      <div class="box-title">📊 Business Line ER Diagram (Schema)</div>
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

    <div>
      <div class="box-title">💡 Preset Analysis Scripts (Click to populate)</div>
      
      <button class="preset-btn" onclick="loadPreset(1)">
        <strong>1. Complex Multi-table JOINs & Aggregations</strong>
        <div class="preset-desc">Calculate profit contribution by product category (joining orders, items, and products).</div>
      </button>

      <button class="preset-btn" onclick="loadPreset(2)">
        <strong>2. Advanced Window Functions</strong>
        <div class="preset-desc">Use RANK() to find the TOP 3 super users by monthly spending.</div>
      </button>

      <button class="preset-btn" onclick="loadPreset(3)">
        <strong>3. CTE (Common Table Expressions)</strong>
        <div class="preset-desc">Use WITH and LAG() functions to calculate the average repurchase cycle of high-value users.</div>
      </button>
    </div>
  </div>

  <div class="box-title">💻 SQL Playground</div>
  <div class="editor-container">
    <textarea id="sql-editor"></textarea>
  </div>
  
  <div class="action-bar">
    <button class="btn-run" onclick="executeSQL()" id="run-btn">🚀 Loading Engine...</button>
    <button class="btn-clear" onclick="clearEditor()">Clear</button>
    <span class="status-badge" id="exec-time"></span>
  </div>

  <div class="result-area" id="result-container">
    <div style="color: #666; text-align: center; margin-top: 1rem;">Query results will appear here...</div>
  </div>

  <div class="sql-footer">
    <p>
      * Disclaimer: The data used on this page is generated entirely by a Python script based on random numbers and preset probabilities; it does not involve any real commercial data.
      <br>
      📥 You can download my data generation script to run it yourself: <a href="/assets/generate_db.py" target="_blank">assets/generate_db.py</a>
      <br>
      📦 Or directly download the SQLite database file used on this page: <a href="/assets/database.sqlite" target="_blank">assets/database.sqlite</a>
    </p>
  </div>

</div>

<script>
  const presets = {
    1: `-- Calculate profit contribution by product category (Completed orders only)
SELECT 
    p.category AS 'Category',
    ROUND(SUM((p.price - p.cost) * oi.quantity), 2) AS 'Total Profit',
    COUNT(DISTINCT o.order_id) AS 'Order Count'
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY [Total Profit] DESC;`,

    2: `-- Find the TOP 3 users by spending for each month
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
        month AS 'Month',
        user_id AS 'User ID',
        user_tier AS 'User Tier',
        ROUND(total_spent, 2) AS 'Monthly Total',
        RANK() OVER(PARTITION BY month ORDER BY total_spent DESC) as rank
    FROM MonthlySpending
)
SELECT * FROM RankedSpending 
WHERE rank <= 3 
ORDER BY Month DESC, rank ASC;`,

    3: `-- Calculate average repurchase cycle for high-value users
WITH UserOrders AS (
    SELECT 
        user_id,
        order_date,
        LAG(order_date) OVER(PARTITION BY user_id ORDER BY order_date) as prev_order_date
    FROM orders
    WHERE status = 'Completed'
)
SELECT 
    u.user_id AS 'User ID',
    u.user_tier AS 'User Tier',
    COUNT(uo.order_date) AS 'Total Orders',
    ROUND(AVG(julianday(uo.order_date) - julianday(uo.prev_order_date)), 1) AS 'Avg Repurchase Cycle (Days)'
FROM UserOrders uo
JOIN users u ON uo.user_id = u.user_id
WHERE uo.prev_order_date IS NOT NULL
GROUP BY u.user_id
HAVING [Total Orders] >= 3
ORDER BY [Avg Repurchase Cycle (Days)] ASC
LIMIT 10;`
  };

  let db = null;
  let editor = null;

  document.addEventListener("DOMContentLoaded", () => {
    editor = CodeMirror.fromTextArea(document.getElementById('sql-editor'), {
      mode: 'text/x-sql',
      theme: 'dracula',
      lineNumbers: true,
      lineWrapping: true,
      viewportMargin: Infinity
    });
    editor.setValue("-- Write your SQL here, or click the preset buttons above\nSELECT * FROM users LIMIT 5;");
    
    initDatabase();
  });

  async function initDatabase() {
    const runBtn = document.getElementById('run-btn');
    try {
      const sqlPromise = initSqlJs({
        locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
      });
      const dataPromise = fetch('/assets/database.sqlite').then(res => {
        if (!res.ok) throw new Error("Unable to load database.sqlite. Please ensure the file is uploaded and not excluded by Jekyll.");
        return res.arrayBuffer();
      });

      const [SQL, buf] = await Promise.all([sqlPromise, dataPromise]);
      db = new SQL.Database(new Uint8Array(buf));
      
      runBtn.innerText = "🚀 Run SQL";
      runBtn.disabled = false;
    } catch (err) {
      runBtn.innerText = "Engine Load Failed";
      runBtn.style.background = "#ef4444";
      document.getElementById('result-container').innerHTML = `<div class="error-msg">Initialization Error: ${err.message}</div>`;
    }
  }

  function loadPreset(id) {
    if(editor) {
      editor.setValue(presets[id]);
      setTimeout(executeSQL, 100);
    }
  }

  function clearEditor() {
    if(editor) editor.setValue("");
    document.getElementById('result-container').innerHTML = `<div style="color: #666; text-align: center; margin-top: 1rem;">Query results will appear here...</div>`;
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
      
      timeBadge.innerText = `⏱️ Execution Time: ${(end - start).toFixed(1)} ms`;
      timeBadge.style.display = 'inline-block';

      if (results.length === 0) {
        resultContainer.innerHTML = '<div style="color: #10b981; margin-top: 1rem;">✅ Execution successful. No rows returned.</div>';
        return;
      }

      let html = '<table class="result-table"><thead><tr>';
      const columns = results[0].columns;
      const values = results[0].values;

      columns.forEach(col => { html += `<th>${col}</th>`; });
      html += '</tr></thead><tbody>';

      values.forEach(row => {
        html += '<tr>';
        row.forEach(val => { 
          let displayVal = val === null ? '<em>NULL</em>' : val;
          html += `<td>${displayVal}</td>`; 
        });
        html += '</tr>';
      });
      html += '</tbody></table>';

      resultContainer.innerHTML = html;

    } catch (err) {
      timeBadge.style.display = 'none';
      resultContainer.innerHTML = `<div class="error-msg">SQL Syntax Error:\n${err.message}</div>`;
    }
  }
</script>
