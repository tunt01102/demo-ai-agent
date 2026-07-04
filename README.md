# Business Analyst Agent - Khoa hoc xay dung AI Agent dau tien

Goi code cho buoi hoc "Xay dung AI Agent tu con so 0" danh cho hoc vien MBA.
Ban se tu tay build mot agent phan tich kinh doanh biet: doc du lieu ban hang
noi bo, tinh toan tai chinh chinh xac, va tra ty gia thoi gian thuc.

## Cai dat (chi lam 1 lan)

### Windows
1. Giai nen goi khoa hoc vao mot thu muc (vd: Documents\ai-agent)
2. Nhay dup chuot vao file: `windows_install.bat`
3. Lam theo huong dan tren man hinh. Script se tu kiem tra may ban,
   tu cai nhung gi con thieu, va hoi ban dan Gemini API key.

### macOS
1. Giai nen goi khoa hoc vao mot thu muc
2. Mo ung dung Terminal (bam Cmd + Space, go "Terminal", Enter)
3. Go `bash ` (co dau cach), keo file `macos_install.sh` tha vao cua so
   Terminal, roi nhan Enter

### Gemini API key (mien phi, khong can the tin dung)
- Lay tai: https://aistudio.google.com/apikey
- Dang nhap Google -> Create API key -> copy chuoi bat dau bang "AIza"
- Neu ban BO QUA buoc nhap key luc cai dat: khong sao, khi chay lab lan dau
  mot trang web se tu mo tren trinh duyet de ban dan key vao.
- Moi nguoi tu tao key rieng, KHONG dung chung key, khong dan key len mang.

## Chay chuong trinh

- Windows: nhay dup file `run_windows.bat`
- macOS:   go `bash run_macos.sh` trong Terminal (dung thu muc khoa hoc)

Menu se hien ra:
1. Kiem tra ket noi  - xac nhan moi truong OK
2. Lab 1             - agent voi "ban mo ta cong viec" (persona)
3. Lab 2             - agent doc du lieu ban hang cua ban (1 tool)
4. Lab 3             - Business Analyst Agent day du (3 tools + vong lap)
5. Nhap / doi API key

## Cau hoi "aha" de thu voi Lab 3

"Tong doanh thu quy 1/2026 cua toi la bao nhieu, tang truong bao nhieu %
so voi quy 4/2025, va quy ra USD theo ty gia hom nay?"

Quan sat: agent tu doc file CSV, tu tinh tang truong bang may tinh,
tu tra ty gia - roi tra loi mot mach. Do la khac biet giua chatbot va agent.

## Danh sach file

| File                  | Vai tro                                          |
|-----------------------|--------------------------------------------------|
| windows_install.bat   | Cai dat tu dong tren Windows                     |
| macos_install.sh      | Cai dat tu dong tren macOS                       |
| run_windows.bat       | Menu chay lab (Windows)                          |
| run_macos.sh          | Menu chay lab (macOS)                            |
| hello_agent.py        | Kiem tra moi truong                              |
| lab1_persona.py       | Bac 1: system prompt = JD cua agent              |
| lab2_one_tool.py      | Bac 2: function calling voi 1 tool               |
| lab3_full_agent.py    | Bac 3: agent hoan chinh 3 tools + vong lap       |
| setup_key.py          | Trang web nhap API key (tu mo khi thieu key)     |
| common.py             | Ham dung chung (doc key, tao client)             |
| sales.csv             | Du lieu ban hang mau (10/2025 - 3/2026, 234 don) |
| requirements.txt      | Danh sach thu vien Python                        |

## Xu ly loi thuong gap

| Trieu chung                                  | Cach xu ly                                              |
|----------------------------------------------|---------------------------------------------------------|
| Windows: "python is not recognized"          | Cai lai Python, TICK o "Add python.exe to PATH"         |
| Windows: go python thi mo Microsoft Store    | Script da tu xu ly bang "py". Neu van loi: cai tu python.org |
| macOS: "command not found: python3"          | Cai Python tu python.org/downloads                      |
| "Key khong hop le"                           | Copy lai key, chu y khong dinh khoang trang o dau/cuoi  |
| Lab bao loi 429 / quota                      | Free tier gioi han so cau hoi moi phut. Doi 1 phut roi hoi tiep |
| Ty gia bao "TY GIA DU PHONG"                 | Mang chan API ty gia. Ket qua van chay, chi la ty gia tham khao |
| Trang nhap key khong tu mo                   | Tu mo trinh duyet, go dia chi in tren Terminal (dang http://127.0.0.1:87xx) |

## Luu y an toan

- File `.env` chua API key cua ban: khong gui cho ai, khong dua len mang,
  khong commit len GitHub.
- Du lieu sales.csv la du lieu HU CAU dung cho hoc tap.
- Free tier cua Gemini co gioi han request/phut - du dung cho buoi hoc,
  khong dung cho san pham that.
