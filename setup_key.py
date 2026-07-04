# setup_key.py
# Trang web nho chay tren may ban (localhost) de nhap Gemini API key.
# Dung khi nguoi dung bo qua buoc nhap key luc cai dat.
# Chi dung thu vien chuan cua Python - khong can cai gi them.
#
# Cach chay truc tiep:  python setup_key.py
# Hoac se tu dong duoc mo khi chay lab ma chua co key.

import http.server
import threading
import urllib.parse
import webbrowser
from pathlib import Path

PORT_START = 8765  # neu ban, tu dong thu 8766..8774
ENV_PATH = Path(__file__).resolve().parent / ".env"

PAGE_FORM = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nhập Gemini API Key</title>
<style>
  :root {{
    --ink: #1c2733;
    --muted: #5b6b7b;
    --line: #d9e0e7;
    --accent: #0b6e4f;
    --accent-soft: #e7f3ee;
    --bg: #f6f8f9;
    --error: #b3261e;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--bg); color: var(--ink);
    font-family: Arial, "Helvetica Neue", sans-serif;
    display: flex; min-height: 100vh; align-items: center; justify-content: center;
    padding: 24px;
  }}
  .card {{
    background: #fff; border: 1px solid var(--line); border-radius: 12px;
    max-width: 560px; width: 100%; padding: 36px 40px;
  }}
  .step-tag {{
    display: inline-block; background: var(--accent-soft); color: var(--accent);
    font-size: 12px; letter-spacing: 1.5px; padding: 4px 10px; border-radius: 999px;
    margin-bottom: 14px; font-weight: bold;
  }}
  h1 {{ font-size: 22px; margin: 0 0 8px; }}
  p.lead {{ color: var(--muted); font-size: 14px; line-height: 1.6; margin: 0 0 22px; }}
  ol {{ color: var(--muted); font-size: 14px; line-height: 1.9; padding-left: 20px; margin: 0 0 24px; }}
  ol a {{ color: var(--accent); }}
  label {{ display: block; font-size: 13px; font-weight: bold; margin-bottom: 6px; }}
  input[type=text] {{
    width: 100%; padding: 12px 14px; font-size: 15px;
    border: 1px solid var(--line); border-radius: 8px;
    font-family: "Courier New", monospace;
  }}
  input[type=text]:focus {{ outline: 2px solid var(--accent); border-color: var(--accent); }}
  button {{
    margin-top: 16px; width: 100%; padding: 13px; font-size: 15px; font-weight: bold;
    background: var(--accent); color: #fff; border: 0; border-radius: 8px; cursor: pointer;
  }}
  button:hover {{ background: #095c42; }}
  .error {{
    background: #fdeceb; border: 1px solid #f2c1bd; color: var(--error);
    padding: 12px 14px; border-radius: 8px; font-size: 13px; margin-bottom: 18px;
    line-height: 1.5;
  }}
  .note {{ font-size: 12px; color: var(--muted); margin-top: 14px; line-height: 1.6; }}
</style>
</head>
<body>
  <div class="card">
    <span class="step-tag">THIẾT LẬP MỘT LẦN</span>
    <h1>Nhập Gemini API Key</h1>
    <p class="lead">Agent cần một chiếc "chìa khóa" để nói chuyện với Gemini. Key này miễn phí và chỉ lưu trên máy của bạn.</p>
    {error_block}
    <ol>
      <li>Mở <a href="https://aistudio.google.com/apikey" target="_blank">aistudio.google.com/apikey</a> (đăng nhập Google)</li>
      <li>Bấm <b>Create API key</b></li>
      <li>Sao chép chuỗi ký tự bắt đầu bằng <b>AIza...</b> và dán vào ô dưới</li>
    </ol>
    <form method="POST" action="/">
      <label for="key">API Key</label>
      <input type="text" id="key" name="key" placeholder="AIza..." autocomplete="off" autofocus>
      <button type="submit">Kiểm tra và lưu key</button>
    </form>
    <p class="note">Key được lưu vào file <b>.env</b> trong thư mục khóa học. Không chia sẻ key cho người khác, không dán key lên mạng.</p>
  </div>
</body>
</html>"""

PAGE_OK = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Đã lưu key</title>
<style>
  body { margin:0; background:#f6f8f9; color:#1c2733; font-family: Arial, sans-serif;
         display:flex; min-height:100vh; align-items:center; justify-content:center; padding:24px; }
  .card { background:#fff; border:1px solid #d9e0e7; border-radius:12px;
          max-width:560px; width:100%; padding:40px; text-align:center; }
  .ok { width:56px; height:56px; border-radius:50%; background:#e7f3ee; color:#0b6e4f;
        font-size:30px; line-height:56px; margin:0 auto 16px; }
  h1 { font-size:22px; margin:0 0 10px; }
  p { color:#5b6b7b; font-size:14px; line-height:1.7; }
  code { background:#eef2f5; padding:2px 8px; border-radius:6px; font-size:13px; }
</style>
</head>
<body>
  <div class="card">
    <div class="ok">&#10003;</div>
    <h1>Key hợp lệ, đã lưu thành công</h1>
    <p>Gemini đã trả lời thử nghiệm thành công.<br>
    Bạn có thể <b>đóng tab này</b> và quay lại cửa sổ Terminal / PowerShell.<br>
    Chương trình sẽ tự chạy tiếp.</p>
  </div>
</body>
</html>"""


def validate_key(key: str):
    """Goi thu Gemini 1 lan de xac nhan key dung. Tra ve (ok, thong_bao_loi)."""
    try:
        from google import genai
        client = genai.Client(api_key=key)
        client.models.generate_content(model="gemini-2.5-flash", contents="ping")
        return True, ""
    except Exception as e:
        msg = str(e)
        if "API_KEY_INVALID" in msg or "API key not valid" in msg:
            return False, "Key không hợp lệ. Kiểm tra lại: key phải bắt đầu bằng AIza và không có khoảng trắng thừa."
        if "PERMISSION" in msg.upper():
            return False, "Key chưa được cấp quyền. Thử tạo key mới trong Google AI Studio."
        return False, "Không kiểm tra được key (có thể do mạng): " + msg[:200]


def save_key(key: str):
    ENV_PATH.write_text(f"GEMINI_API_KEY={key}\n", encoding="utf-8")


class _Handler(http.server.BaseHTTPRequestHandler):
    error_message = ""

    def _send(self, html: str, status: int = 200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        err = ""
        if _Handler.error_message:
            err = f'<div class="error">{_Handler.error_message}</div>'
            _Handler.error_message = ""
        self._send(PAGE_FORM.format(error_block=err))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8"))
        key = data.get("key", [""])[0].strip()

        if not key:
            _Handler.error_message = "Bạn chưa dán key vào ô nhập."
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            return

        print("Dang kiem tra key voi Gemini...")
        ok, err = validate_key(key)
        if ok:
            save_key(key)
            print("Key hop le. Da luu vao .env")
            self._send(PAGE_OK)
            # Tat server sau khi da tra loi xong
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            print("Key khong hop le:", err)
            _Handler.error_message = err
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

    def log_message(self, *args):
        pass  # tat log http cho do roi mat nguoi hoc


def _find_free_port() -> int:
    """Quet port trong tu 8765; neu tat ca ban, de he dieu hanh tu chon."""
    import socket
    for port in range(PORT_START, PORT_START + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return 0  # port 0 = he dieu hanh tu cap port trong


def run():
    """Mo trang nhap key va CHO den khi nguoi dung nhap key hop le."""
    server = http.server.ThreadingHTTPServer(("127.0.0.1", _find_free_port()), _Handler)
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"Trang nhap key: {url}")
    print("(Neu trinh duyet khong tu mo, hay tu go dia chi tren vao trinh duyet)")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    server.serve_forever()  # dung lai khi key duoc luu (shutdown o tren)
    server.server_close()


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv(ENV_PATH)
    if os.getenv("GEMINI_API_KEY", "").strip():
        ans = input("Da co key trong .env. Nhap key moi de thay the? (y/n): ").strip().lower()
        if ans != "y":
            print("Giu nguyen key cu. Thoat.")
            raise SystemExit(0)
    run()
    print("Xong. Bay gio ban co the chay cac lab.")
