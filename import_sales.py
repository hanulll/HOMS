from pathlib import Path
import sqlite3

# ===========================
# 경로 설정
# ===========================

DB_PATH = Path.home() / "HOMS/database/HOMS.db"
SALES_DIR = Path.home() / "koms_data/sales_2355"

print("=" * 40)
print(" HOMS 판매데이터 수집기 ")
print("=" * 40)

print(f"DB : {DB_PATH}")
print(f"매출폴더 : {SALES_DIR}")

# DB 연결
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 최신 엑셀 찾기
files = sorted(SALES_DIR.glob("*.xlsx"))

if not files:
    print("매출파일이 없습니다.")
    exit()

latest = files[-1]

print(f"\n최신파일 : {latest.name}")

conn.close()

print("\n1단계 완료")

from openpyxl import load_workbook

print("\n엑셀 분석 시작...")

wb = load_workbook(latest, data_only=True)

print("\n시트 목록")

for sheet in wb.sheetnames:
    print("-", sheet)

ws = wb[wb.sheetnames[0]]

print("\n첫 15행")

for row in ws.iter_rows(max_row=15, values_only=True):
    print(row)
