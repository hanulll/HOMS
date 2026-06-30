import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "HOMS.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 판매기록
cur.execute("""
CREATE TABLE IF NOT EXISTS sales(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_date TEXT,
    menu_name TEXT,
    qty REAL,
    source TEXT
)
""")

# 발주기록
cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT,
    item_name TEXT,
    qty REAL
)
""")

# 재고기록
cur.execute("""
CREATE TABLE IF NOT EXISTS inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_date TEXT,

    drum REAL,
    wing REAL,
    whole REAL,

    honey_combo REAL,
    honey_boneless REAL,
    boneless REAL,
    thailand_wing REAL
)
""")

# AI 예측
cur.execute("""
CREATE TABLE IF NOT EXISTS forecast(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    forecast_date TEXT,
    item_name TEXT,

    predicted REAL,
    actual REAL,

    error REAL,
    confidence REAL
)
""")

# 날씨
cur.execute("""
CREATE TABLE IF NOT EXISTS weather(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    weather_date TEXT,
    rain REAL,
    temp REAL,
    weather TEXT
)
""")

# 이벤트
cur.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_date TEXT,
    event_name TEXT,
    impact REAL
)
""")

# 로그
cur.execute("""
CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    log_time TEXT,
    category TEXT,
    message TEXT
)
""")

conn.commit()
conn.close()

print("=================================")
print("      HOMS DATABASE CREATED")
print("=================================")
print(DB_PATH)
