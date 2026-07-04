# lab2_one_tool.py
# ============================================================
# BAC 2: TRAO CHO AGENT CONG CU DAU TIEN (FUNCTION CALLING)
# ============================================================
# Van de: ChatGPT/Gemini KHONG biet du lieu noi bo cua ban.
# Giai phap: viet 1 ham Python doc file sales.csv, roi "khai bao"
# ham do cho Gemini. Khi ban hoi ve doanh thu, Gemini se TU QUYET DINH
# goi ham nay - do chinh la ranh gioi giua chatbot va agent.
#
# Quy trinh 4 buoc (in ra man hinh de ban quan sat):
#   1. Ban hoi  ->  2. Gemini yeu cau goi tool  ->
#   3. Code cua ban chay tool  ->  4. Gemini doc ket qua va tra loi

import csv
from collections import defaultdict
from pathlib import Path

from google.genai import types

from common import make_client, MODEL, friendly_api_error

CSV_PATH = Path(__file__).resolve().parent / "sales.csv"


# ============================================================
# PHAN 1: VIET TOOL (ham Python binh thuong)
# ============================================================
def read_sales_data(period: str = "all", group_by: str = "none") -> dict:
    """Doc va tong hop du lieu tu sales.csv.

    period:   "all" | "2025-Q4" | "2026-Q1" | thang dang "2026-01"
    group_by: "none" | "san_pham" | "khu_vuc" | "thang"
    """
    if not CSV_PATH.exists():
        return {"loi": "Khong tim thay file sales.csv"}

    def in_period(ngay: str) -> bool:
        if period == "all":
            return True
        if period == "2025-Q4":
            return "2025-10" <= ngay[:7] <= "2025-12"
        if period == "2026-Q1":
            return "2026-01" <= ngay[:7] <= "2026-03"
        return ngay[:7] == period  # dang "2026-01"

    tong_doanh_thu = 0
    tong_don = 0
    nhom = defaultdict(int)

    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not in_period(row["ngay"]):
                continue
            dt = int(row["doanh_thu_vnd"])
            tong_doanh_thu += dt
            tong_don += 1
            if group_by == "san_pham":
                nhom[row["san_pham"]] += dt
            elif group_by == "khu_vuc":
                nhom[row["khu_vuc"]] += dt
            elif group_by == "thang":
                nhom[row["ngay"][:7]] += dt

    ket_qua = {
        "ky": period,
        "tong_doanh_thu_vnd": tong_doanh_thu,
        "so_don_hang": tong_don,
    }
    if group_by != "none":
        ket_qua["chi_tiet_theo_" + group_by] = dict(
            sorted(nhom.items(), key=lambda x: -x[1])
        )
    return ket_qua


# ============================================================
# PHAN 2: KHAI BAO TOOL CHO GEMINI (nhu viet mo ta cong cu
# trong so tay nhan vien - mo ta cang ro, agent dung cang dung)
# ============================================================
sales_tool = types.FunctionDeclaration(
    name="read_sales_data",
    description=(
        "Doc va tong hop du lieu ban hang noi bo cua cong ty tu file sales.csv. "
        "Du lieu co tu thang 10/2025 den thang 3/2026. "
        "Dung tool nay moi khi nguoi dung hoi ve doanh thu, don hang, "
        "san pham hay khu vuc cua CONG TY."
    ),
    parameters={
        "type": "object",
        "properties": {
            "period": {
                "type": "string",
                "description": 'Ky bao cao: "all", "2025-Q4", "2026-Q1", hoac thang dang "2026-01"',
            },
            "group_by": {
                "type": "string",
                "description": 'Nhom theo: "none", "san_pham", "khu_vuc", "thang"',
            },
        },
    },
)

SYSTEM_PROMPT = """Ban la chuyen vien phan tich kinh doanh cua cong ty.
Khi nguoi dung hoi ve so lieu cua cong ty, PHAI dung tool read_sales_data,
tuyet doi khong bia so. Tra loi tieng Viet, ngan gon, co so lieu cu the.
Doanh thu hien thi kem don vi VND va dinh dang co dau phay ngan cach."""

# ============================================================
# PHAN 3: VONG HOI THOAI
# ============================================================
client = make_client()
chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(function_declarations=[sales_tool])],
    ),
)

print("=" * 60)
print("LAB 2 - Agent co cong cu dau tien: doc du lieu ban hang")
print("Go 'exit' de thoat.")
print("Goi y: 'Tong doanh thu quy 1 nam 2026 la bao nhieu?'")
print("       'Khu vuc nao ban tot nhat trong quy 1?'")
print("=" * 60)

while True:
    user_input = input("\nBan: ").strip()
    if user_input.lower() in ("exit", "quit", "thoat"):
        break
    if not user_input:
        continue

    try:
        response = chat.send_message(user_input)

        # Kiem tra: Gemini co yeu cau goi tool khong?
        while response.function_calls:
            fc = response.function_calls[0]
            print(f"\n   [AGENT QUYET DINH] goi tool: {fc.name}({dict(fc.args)})")

            ket_qua = read_sales_data(**dict(fc.args))  # code cua BAN chay tool
            print(f"   [TOOL TRA VE] {ket_qua}")

            # Gui ket qua nguoc lai cho Gemini de no viet cau tra loi
            response = chat.send_message(
                types.Part.from_function_response(
                    name=fc.name, response={"result": ket_qua}
                )
            )

        print("\nAgent:", response.text)
    except Exception as e:
        print("\n[LOI]", friendly_api_error(e))
