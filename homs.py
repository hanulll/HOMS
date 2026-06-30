import os

print("=" * 34)
print("        HOMS v0.21")
print("=" * 34)

while True:

    print("\n1. 판매데이터 가져오기")
    print("2. 재고 입력")
    print("3. 발주 계산")
    print("4. DB 상태")
    print("5. 백업")
    print("6. 종료")

    menu = input("\n선택 : ")

    if menu == "1":
        os.system("python3 /home/hanul/HOMS/import_sales.py")

    elif menu == "2":
        print("▶ 재고 입력 (준비중)")

    elif menu == "3":
        print("▶ 발주 계산 (준비중)")

    elif menu == "4":
        print("▶ DB 상태 (준비중)")

    elif menu == "5":
        print("▶ 백업 (준비중)")

    elif menu == "6":
        print("\nHOMS 종료")
        break

    else:
        print("\n잘못된 메뉴입니다.")
