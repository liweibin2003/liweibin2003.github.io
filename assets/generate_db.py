import sqlite3
import random
from datetime import datetime, timedelta

# 1. 连接并创建 SQLite 文件
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

# 2. 创建表结构 (DDL)
cursor.executescript('''
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS users;

    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        register_date DATE,
        user_tier VARCHAR(20)
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category VARCHAR(50),
        price DECIMAL(10,2),
        cost DECIMAL(10,2)
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_date DATE,
        status VARCHAR(20),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE order_items (
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
''')

# 3. 插入测试数据
# 预设维度
tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports']
statuses = ['Completed', 'Completed', 'Completed', 'Pending', 'Cancelled'] # 增加 Completed 的权重

# 生成 20 个商品
products_data = []
for _ in range(20):
    cat = random.choice(categories)
    cost = round(random.uniform(10.0, 200.0), 2)
    price = round(cost * random.uniform(1.2, 2.5), 2) # 保证售价高于成本
    products_data.append((cat, price, cost))
cursor.executemany('INSERT INTO products (category, price, cost) VALUES (?, ?, ?)', products_data)

# 生成 200 个用户
users_data = []
start_date = datetime(2022, 1, 1)
for _ in range(200):
    reg_date = start_date + timedelta(days=random.randint(0, 700))
    tier = random.choices(tiers, weights=[50, 30, 15, 5])[0] # 根据权重分配等级
    users_data.append((reg_date.strftime('%Y-%m-%d'), tier))
cursor.executemany('INSERT INTO users (register_date, user_tier) VALUES (?, ?)', users_data)

# 生成 800 个订单及明细
for _ in range(800):
    user_id = random.randint(1, 200)
    # 简单的逻辑：订单日期必须在注册日期之后，这里简化为2023-2024的随机日期
    order_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
    status = random.choice(statuses)
    
    cursor.execute('INSERT INTO orders (user_id, order_date, status) VALUES (?, ?, ?)', 
                   (user_id, order_date.strftime('%Y-%m-%d'), status))
    order_id = cursor.lastrowid
    
    # 每个订单随机 1-3 种商品明细
    num_items = random.randint(1, 3)
    selected_products = random.sample(range(1, 21), num_items)
    for prod_id in selected_products:
        quantity = random.randint(1, 5)
        cursor.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', 
                       (order_id, prod_id, quantity))

# 4. 提交并关闭
conn.commit()
conn.close()
print("成功生成 database.sqlite 文件，包含 4 张表和近 1000 条测试数据。")
