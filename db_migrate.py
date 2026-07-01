"""
==========================================================
HOMS Database Migration
==========================================================
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "database" / "homs.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()


def add_column(table, column, column_type):

    cols = [
        row[1]
        for row in cur.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()
    ]

    if column in cols:
        print(f"[SKIP] {table}.{column}")
        return

    cur.execute(
        f"""
        ALTER TABLE {table}
        ADD COLUMN {column} {column_type}
        """
    )

    print(f"[ADD] {table}.{column}")


add_column(
    "order_history",
    "delivery_date",
    "TEXT",
)

add_column(
    "order_history",
    "received_date",
    "TEXT",
)

add_table_sql = """
CREATE TABLE IF NOT EXISTS receipt_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_date TEXT NOT NULL,
    file_name TEXT NOT NULL,
    ingredient TEXT NOT NULL,
    quantity REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

cur.execute(add_table_sql)

print("[OK] receipt_history")

conn.commit()

# ----------------------------------------------------------
# PREP INVENTORY
# ----------------------------------------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS prep_inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT UNIQUE,
    quantity REAL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ----------------------------------------------------------
# PREP HISTORY
# ----------------------------------------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS prep_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prep_date TEXT,
    product TEXT,
    remaining_before REAL,
    target_sales REAL,
    ai_adjustment REAL,
    recommended REAL,
    prepared REAL,
    worker TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ----------------------------------------------------------
# WEEKLY INVENTORY CHECK
# ----------------------------------------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS weekly_inventory_check(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_date TEXT,
    ingredient TEXT,
    ai_quantity REAL,
    actual_quantity REAL,
    difference REAL,
    accuracy REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

conn.close()

print()
print("Migration Complete")

