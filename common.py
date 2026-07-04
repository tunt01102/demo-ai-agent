# common.py
# Ham dung chung cho tat ca cac lab.
# Nhiem vu: doc GEMINI_API_KEY tu file .env.
# Neu chua co key -> tu dong mo trang web de nguoi dung nhap key.

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# File .env nam cung thu muc voi code
ENV_PATH = Path(__file__).resolve().parent / ".env"

MODEL = "gemini-2.5-flash"  # model free tier, doi o day neu Google doi ten model


def get_api_key() -> str:
    """Tra ve API key. Neu chua co, mo trang web cho nguoi dung nhap."""
    load_dotenv(ENV_PATH)
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if key:
        return key

    print("")
    print("Chua tim thay Gemini API key.")
    print("Dang mo trang web de ban nhap key (nhin sang trinh duyet)...")
    print("")

    import setup_key  # import tai day de tranh vong lap import
    setup_key.run()  # ham nay CHO den khi nguoi dung nhap key xong

    # Doc lai .env sau khi trang web da luu key
    load_dotenv(ENV_PATH, override=True)
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        print("Van chua co key hop le. Thoat chuong trinh.")
        sys.exit(1)
    return key


def make_client():
    """Tao Gemini client da gan key."""
    from google import genai
    return genai.Client(api_key=get_api_key())


def friendly_api_error(e: Exception) -> str:
    """Dich loi API thanh thong bao de hieu cho nguoi hoc."""
    msg = str(e)
    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
        return ("Gemini free tier gioi han so cau hoi moi phut. "
                "Doi khoang 1 phut roi hoi tiep nhe.")
    if "API_KEY_INVALID" in msg or "API key not valid" in msg:
        return ("API key khong hop le. Chay lai menu, chon muc 5 de nhap key moi.")
    if "503" in msg or "UNAVAILABLE" in msg:
        return "May chu Gemini dang qua tai. Thu lai sau vai giay."
    return "Loi khi goi Gemini: " + msg[:300]
