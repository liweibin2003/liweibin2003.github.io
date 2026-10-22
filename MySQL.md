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
  .preset-btn { display: block; width: 100%; text-align: left; padding: 0.75rem 1rem; margin-bottom: 0.75rem; background: #fff; border: 1px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 0.9rem; color: #1f2937; }
  .preset-btn:hover { border-color: #3b82f6; background: #eff6ff; color: #1d4ed8; }
  .preset-desc { font-size: 0.8rem; color: #6b7280; margin-top: 0.25rem; }
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
  /* Fixed text color to override theme settings */
  .result-table th, .result-table td { padding: 0.75rem; border-bottom: 1px solid #eee; color: #1f2937 !important; }
  .result-table th { background: #f9fafb; font-weight: 600; white-space: nowrap; }
  .error-msg { color: #dc2626; font-family: monospace; white-space: pre-wrap; }
  .sql-footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px dashed #ccc; font-size: 0.85rem; color: #6b7280; }
  .sql-footer a { color: #3b82f6; text-decoration: none; }
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
    <strong>Geek Note:</strong> This page operates entirely without backend servers. The SQL engine runs locally in your browser's memory via WebAssembly (sql.js). It uses SQLite under the hood, perfectly supporting core standard SQL, multi-table JOINs, and Window Functions.
  </div>

  <div class="sql-layout">
    <div>
      <div class="box-title">📊 Business ER Diagram (Schema)</div>
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
      <div class="box-title">💡 Preset Scenarios (Click to Load)</div>
      
      <button class="preset-btn" onclick="loadPreset(1)">
        <strong>1. Complex JOINs & Aggregation</strong>
        <div class="preset-desc">Calculate profit contribution by product category (joins 3 tables).</div>
      </button>

      <button class="preset-btn" onclick="loadPreset(2)">
        <strong>2. Advanced Window Functions</strong>
        <div class="preset-desc">Use RANK() to find the top 3 spending users for each month.</div>
      </button>

      <button class="preset-btn" onclick="loadPreset(3)">
        <strong>3. CTE (Common Table Expressions)</strong>
        <div class="preset-desc">Use WITH and LAG() to calculate average repurchase cycles for high-value users.</div>
      </button>
    </div>
  </div>

  <div class="box-title">💻 SQL Playground (Write your own queries!)</div>
  <div class="editor-container">
    <textarea id="sql-editor"></textarea>
  </div>
  
  <div class="action-bar">
    <button class="btn-run" onclick="executeSQL()" id="run-btn">🚀 Loading Engine...</button>
    <button class="btn-clear" onclick="clearEditor()">Clear</button>
    <span class="status-badge" id="exec-time"></span>
  </div>

  <div class="result-area" id="result-container">
    <div style="color: #6b7280; text-align: center; margin-top: 1rem;">Query results will appear here...</div>
  </div>

  <div class="sql-footer">
    <p>
      * Disclaimer: The data used on this page is randomly generated via a Python script and does not represent any real commercial data.
      <br>
      📥 Download the data generation script to run yourself: <a href="/assets/generate_db.py" target="_blank">assets/generate_db.py</a>
      <br>
      📦 Or download the raw SQLite database file used here: <a href="/assets/database.sqlite" target="_blank">assets/database.sqlite</a>
    </p>
  </div>

</div>

<script>
  const presets = {
    1: `-- Calculate profit contribution by category (completed orders only)
SELECT 
    p.category AS 'Category',
    ROUND(SUM((p.price - p.cost) * oi.quantity), 2) AS 'Total_Profit',
    COUNT(DISTINCT o.order_id) AS 'Order_Count'
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY Total_Profit DESC;`,

    2: `-- Find the top 3 spending users per month using Window Functions
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
        user_id AS 'User_ID',
        user_tier AS 'User_Tier',
        ROUND(total_spent, 2) AS 'Monthly_Spent',
        RANK() OVER(PARTITION BY month ORDER BY total_spent DESC) as rank
    FROM MonthlySpending
)
SELECT * FROM RankedSpending 
WHERE rank <= 3 
ORDER BY Month DESC, rank ASC;`,

    3: `-- Calculate average repurchase cycle (days between orders) for active users
WITH UserOrders AS (
    SELECT 
        user_id,
        order_date,
        LAG(order_date) OVER(PARTITION BY user_id ORDER BY order_date) as prev_order_date
    FROM orders
    WHERE status = 'Completed'
)
SELECT 
    u.user_id AS 'User_ID',
    u.user_tier AS 'User_Tier',
    COUNT(uo.order_date) AS 'Total_Orders',
    ROUND(AVG(julianday(uo.order_date) - julianday(uo.prev_order_date)), 1) AS 'Avg_Repurchase_Days'
FROM UserOrders uo
JOIN users u ON uo.user_id = u.user_id
WHERE uo.prev_order_date IS NOT NULL
GROUP BY u.user_id
HAVING Total_Orders >= 3
ORDER BY Avg_Repurchase_Days ASC
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
    editor.setValue("-- Write your own SQL here, or click a preset button above to load an example.\nSELECT * FROM users LIMIT 5;");
    
    initDatabase();
  });

  async function initDatabase() {
    const runBtn = document.getElementById('run-btn');
    try {
      const sqlPromise = initSqlJs({
        locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
      });
      const dataPromise = fetch('/assets/database.sqlite').then(res => {
        if (!res.ok) throw new Error("Failed to load database.sqlite. Please ensure the file is uploaded and not excluded by Jekyll.");
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
    document.getElementById('result-container').innerHTML = `<div style="color: #6b7280; text-align: center; margin-top: 1rem;">Query results will appear here...</div>`;
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
        resultContainer.innerHTML = '<div style="color: #10b981; margin-top: 1rem;">✅ Query executed successfully (0 rows returned).</div>';
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
