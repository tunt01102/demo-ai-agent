# hello_agent.py
# Muc dich: kiem tra moi truong da san sang chua.
# Neu ban thay Gemini tra loi = moi truong OK, san sang hoc lab.

from common import make_client, MODEL, friendly_api_error

print("Dang ket noi toi Gemini...")
client = make_client()

try:
    response = client.models.generate_content(
        model=MODEL,
        contents="Chao ban bang 1 cau tieng Viet ngan, xac nhan ket noi thanh cong.",
    )
    print("")
    print("GEMINI TRA LOI:", response.text)
    print("")
    print("=> Moi truong da san sang. Ban co the chay lab1_persona.py")
except Exception as e:
    print("")
    print("[CHUA KET NOI DUOC]", friendly_api_error(e))
