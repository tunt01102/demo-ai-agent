# lab1_persona.py
# ============================================================
# BAC 1: SYSTEM PROMPT = BAN MO TA CONG VIEC (JD) CUA AGENT
# ============================================================
# Y tuong: khi tuyen mot nhan vien, ban viet JD cang ro thi
# nhan vien lam viec cang dung y. Agent cung vay: system prompt
# la JD cua no.
#
# BAI TAP: chay thu, sau do SUA doan SYSTEM_PROMPT ben duoi
# (vi du: doi thanh chuyen gia marketing, doi giong dieu,
# them gioi han "khong tra loi ngoai chu de kinh doanh")
# roi chay lai va quan sat hanh vi thay doi.

from google.genai import types

from common import make_client, MODEL, friendly_api_error

# ----- JD cua agent: SUA O DAY -----
SYSTEM_PROMPT = """Ban la mot chuyen vien phan tich kinh doanh (Business Analyst)
lam viec cho mot cong ty ban le tai Viet Nam.

Nhiem vu:
- Tra loi ngan gon, di thang vao van de, dung ngon ngu kinh doanh.
- Khi dua ra nhan dinh, luon neu ro can cu.
- Neu khong du thong tin, noi ro la khong du thong tin va can gi them.
- Tra loi bang tieng Viet.

Gioi han:
- Khong bia so lieu.
- Khong tu van phap ly hay thue.
"""
# -----------------------------------

client = make_client()

chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
)

print("=" * 60)
print("LAB 1 - Agent voi ban mo ta cong viec (persona)")
print("Go cau hoi va nhan Enter. Go 'exit' de thoat.")
print("Goi y cau hoi thu: 'Cong ty toi doanh thu giam 2 thang lien,")
print("toi nen bat dau phan tich tu dau?'")
print("=" * 60)

while True:
    user_input = input("\nBan: ").strip()
    if user_input.lower() in ("exit", "quit", "thoat"):
        print("Tam biet!")
        break
    if not user_input:
        continue
    try:
        response = chat.send_message(user_input)
        print("\nAgent:", response.text)
    except Exception as e:
        print("\n[LOI]", friendly_api_error(e))
