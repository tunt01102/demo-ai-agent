# lab3_full_agent.py
# ============================================================
# BAC 3: BUSINESS ANALYST AGENT HOAN CHINH (3 TOOLS + VONG LAP)
# ============================================================
# Agent nay co 3 cong cu, moi cong cu giai quyet 1 diem yeu
# co huu cua chatbot:
#   1. read_sales_data     -> chatbot khong biet du lieu noi bo cua ban
#   2. financial_calculator -> chatbot tinh nham khong tin cay
#   3. get_exchange_rate   -> chatbot khong biet thong tin hien tai
#
# Diem moi so voi Lab 2: VONG LAP AGENT. Mot cau hoi phuc tap
# co the can goi NHIEU tool noi tiep nhau. Agent tu quyet dinh
# goi tool nao, theo thu tu nao, den khi du thong tin de tra loi.
#
# Cau hoi "aha" de thu sau khi chay:
#   "Tong doanh thu quy 1/2026 cua toi la bao nhieu, tang truong
#    bao nhieu % so voi quy 4/2025, va quy ra USD theo ty gia hom nay?"

import csv
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

from google.genai import types

from common import make_client, MODEL, friendly_api_error

CSV_PATH = Path(__file__).resolve().parent / "sales.csv"

# Ty gia du phong khi khong goi duoc API (vd: mang lop hoc chan)
FALLBACK_USD_VND = 25400.0


# ============================================================
# TOOL 1: doc du lieu ban hang noi bo
# ============================================================
def read_sales_data(period: str = "all", group_by: str = "none") -> dict:
    """Doc va tong hop sales.csv theo ky va nhom."""
    if not CSV_PATH.exists():
        return {"loi": "Khong tim thay file sales.csv"}

    def in_period(ngay: str) -> bool:
        if period == "all":
            return True
        if period == "2025-Q4":
            return "2025-10" <= ngay[:7] <= "2025-12"
        if period == "2026-Q1":
            return "2026-01" <= ngay[:7] <= "2026-03"
        return ngay[:7] == period

    tong, so_don = 0, 0
    nhom = defaultdict(int)
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not in_period(row["ngay"]):
                continue
            dt = int(row["doanh_thu_vnd"])
            tong += dt
            so_don += 1
            if group_by == "san_pham":
                nhom[row["san_pham"]] += dt
            elif group_by == "khu_vuc":
                nhom[row["khu_vuc"]] += dt
            elif group_by == "thang":
                nhom[row["ngay"][:7]] += dt

    kq = {"ky": period, "tong_doanh_thu_vnd": tong, "so_don_hang": so_don}
    if group_by != "none":
        kq["chi_tiet_theo_" + group_by] = dict(sorted(nhom.items(), key=lambda x: -x[1]))
    return kq


# ============================================================
# TOOL 2: may tinh tai chinh (tinh CHINH XAC, khong tinh nham)
# ============================================================
def financial_calculator(expression: str) -> dict:
    """Tinh mot bieu thuc so hoc, vd: "(651638091 - 555531249) / 555531249 * 100".
    Chi cho phep so va cac phep + - * / ( ) . de dam bao an toan."""
    if not re.fullmatch(r"[0-9+\-*/(). eE]+", expression):
        return {"loi": "Bieu thuc chua ky tu khong hop le. Chi dung so va + - * / ( )"}
    try:
        ket_qua = eval(expression, {"__builtins__": {}}, {})  # da loc ky tu o tren
        return {"bieu_thuc": expression, "ket_qua": ket_qua}
    except Exception as e:
        return {"loi": f"Khong tinh duoc: {e}"}


# ============================================================
# TOOL 3: ty gia thoi gian thuc (chatbot khong biet "hom nay")
# ============================================================
def get_exchange_rate(base: str = "USD", target: str = "VND") -> dict:
    """Lay ty gia hien tai tu API mien phi open.er-api.com (khong can key).
    Neu mang loi -> dung ty gia du phong va bao ro cho nguoi dung."""
    url = f"https://open.er-api.com/v6/latest/{base.upper()}"
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        rate = data["rates"][target.upper()]
        return {
            "cap_ty_gia": f"{base.upper()}/{target.upper()}",
            "ty_gia": rate,
            "nguon": "open.er-api.com (thoi gian thuc)",
            "cap_nhat": data.get("time_last_update_utc", ""),
        }
    except Exception as e:
        return {
            "cap_ty_gia": f"{base.upper()}/{target.upper()}",
            "ty_gia": FALLBACK_USD_VND if base.upper() == "USD" else None,
            "nguon": "TY GIA DU PHONG - khong goi duoc API",
            "canh_bao": f"Loi mang: {str(e)[:120]}. Ket qua chi mang tinh tham khao.",
        }


# Bang tra: ten tool -> ham Python tuong ung
TOOLS = {
    "read_sales_data": read_sales_data,
    "financial_calculator": financial_calculator,
    "get_exchange_rate": get_exchange_rate,
}


# ============================================================
# KHAI BAO 3 TOOL CHO GEMINI
# ============================================================
declarations = [
    types.FunctionDeclaration(
        name="read_sales_data",
        description=(
            "Doc va tong hop du lieu ban hang noi bo cua cong ty (sales.csv, "
            "tu 10/2025 den 3/2026). Dung khi nguoi dung hoi ve doanh thu, "
            "don hang, san pham, khu vuc cua cong ty."
        ),
        parameters={
            "type": "object",
            "properties": {
                "period": {
                    "type": "string",
                    "description": '"all", "2025-Q4", "2026-Q1", hoac thang "2026-01"',
                },
                "group_by": {
                    "type": "string",
                    "description": '"none", "san_pham", "khu_vuc", "thang"',
                },
            },
        },
    ),
    types.FunctionDeclaration(
        name="financial_calculator",
        description=(
            "Tinh toan so hoc CHINH XAC (tang truong %, bien loi nhuan, quy doi...). "
            "LUON dung tool nay cho moi phep tinh, khong duoc tu tinh nham. "
            'Vi du tinh tang truong: "(gia_tri_moi - gia_tri_cu) / gia_tri_cu * 100"'
        ),
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": 'Bieu thuc so hoc, vd "(120 - 100) / 100 * 100"',
                }
            },
            "required": ["expression"],
        },
    ),
    types.FunctionDeclaration(
        name="get_exchange_rate",
        description=(
            "Lay ty gia hoi doai HIEN TAI (thoi gian thuc). Dung khi can quy doi "
            "tien te theo ty gia hom nay, vi du USD sang VND."
        ),
        parameters={
            "type": "object",
            "properties": {
                "base": {"type": "string", "description": 'Ma tien goc, vd "USD"'},
                "target": {"type": "string", "description": 'Ma tien dich, vd "VND"'},
            },
        },
    ),
]

SYSTEM_PROMPT = """Ban la Business Analyst Agent cua mot cong ty ban le Viet Nam.

Quy tac lam viec:
1. So lieu cong ty: PHAI lay tu tool read_sales_data, khong bia so.
2. Moi phep tinh (tang truong %, quy doi, ty le): PHAI dung financial_calculator.
3. Ty gia: PHAI dung get_exchange_rate. Neu tool bao dung ty gia du phong,
   phai noi ro dieu do trong cau tra loi.
4. Tra loi tieng Viet, ngan gon nhu bao cao cho sep: so lieu cu the,
   co don vi, co nhan xet 1-2 cau neu phu hop.
"""

# ============================================================
# VONG LAP AGENT: trai tim cua bai hoc
# ============================================================
client = make_client()
chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(function_declarations=declarations)],
    ),
)

print("=" * 62)
print("LAB 3 - Business Analyst Agent (3 tools). Go 'exit' de thoat.")
print("Cau hoi 'aha' de thu:")
print('  "Tong doanh thu quy 1/2026 cua toi la bao nhieu, tang truong')
print('   bao nhieu % so voi quy 4/2025, va quy ra USD ty gia hom nay?"')
print("=" * 62)

while True:
    user_input = input("\nBan: ").strip()
    if user_input.lower() in ("exit", "quit", "thoat"):
        break
    if not user_input:
        continue

    try:
        response = chat.send_message(user_input)

        # VONG LAP: chay den khi Gemini khong yeu cau tool nao nua
        buoc = 0
        while response.function_calls:
            buoc += 1
            parts = []
            for fc in response.function_calls:
                print(f"\n   [BUOC {buoc}] Agent goi: {fc.name}({dict(fc.args)})")
                ham = TOOLS.get(fc.name)
                ket_qua = ham(**dict(fc.args)) if ham else {"loi": "tool khong ton tai"}
                print(f"   [KET QUA ] {ket_qua}")
                parts.append(
                    types.Part.from_function_response(
                        name=fc.name, response={"result": ket_qua}
                    )
                )
            response = chat.send_message(parts)

        print("\nAgent:", response.text)
    except Exception as e:
        print("\n[LOI]", friendly_api_error(e))
