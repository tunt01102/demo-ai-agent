#!/usr/bin/env bash
# ============================================================
# macos_install.sh - Cai dat tu dong Business Analyst Agent (macOS)
# Cach chay: mo Terminal, go "bash " roi keo file nay vao, Enter
# ============================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
VENV="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

# -- Gatekeeper: xoa co quarantine de double-click hoat dong binh thuong -----
xattr -dr com.apple.quarantine "$SCRIPT_DIR" 2>/dev/null || true
chmod +x "$0" 2>/dev/null || true

line() { echo "  ------------------------------------------------"; }
fail_exit() {
    echo ""
    echo " [LOI]  $1"
    [ -n "${2:-}" ] && echo "   -->  $2"
    echo ""
    echo "  Sua theo huong dan tren roi chay lai: bash macos_install.sh"
    echo "  Nhan Enter de dong..."
    read -r || true
    exit 1
}

echo ""
echo "  +--------------------------------------------------+"
echo "  |   CAI DAT BUSINESS ANALYST AGENT  --  macOS      |"
echo "  +--------------------------------------------------+"
echo ""

_python_ok() {
    local bin="$1"
    command -v "$bin" &>/dev/null || [ -x "$bin" ] || return 1
    "$bin" -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" 2>/dev/null
}

# ============================================================
# BUOC 1: Tim Python 3.10+ (tu dong cai neu khong thay)
# ============================================================
echo "  [1/5] Tim Python 3.10+..."
line

PYTHON=""

# 1a. Cac lenh co san trong PATH
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if _python_ok "$candidate"; then PYTHON="$candidate"; break; fi
done

# 1b. Duong dan Homebrew (Apple Silicon + Intel) va Python.framework
if [ -z "$PYTHON" ]; then
    for p in \
        /opt/homebrew/opt/python@3.13/bin/python3.13 \
        /opt/homebrew/opt/python@3.12/bin/python3.12 \
        /opt/homebrew/opt/python@3.11/bin/python3.11 \
        /opt/homebrew/opt/python@3.10/bin/python3.10 \
        /opt/homebrew/bin/python3 \
        /usr/local/opt/python@3.13/bin/python3.13 \
        /usr/local/opt/python@3.12/bin/python3.12 \
        /usr/local/opt/python@3.11/bin/python3.11 \
        /usr/local/opt/python@3.10/bin/python3.10 \
        /usr/local/bin/python3 \
        /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 \
        /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 \
        /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 \
        /Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10
    do
        if _python_ok "$p"; then PYTHON="$p"; break; fi
    done
fi

# 1c. Tu dong cai neu van chua co: brew -> tai .pkg tu python.org
if [ -z "$PYTHON" ]; then
    echo "   [!]  Khong tim thay Python 3.10+ -- thu cai tu dong..."
    if command -v brew &>/dev/null; then
        echo "   -->  Homebrew tim thay. Dang cai Python 3.12..."
        brew install python@3.12 2>&1 | grep -E "(Already installed|Pouring|Installing|Error|Warning)" || true
        brew link --overwrite python@3.12 2>/dev/null || true
        for p in \
            /opt/homebrew/opt/python@3.12/bin/python3.12 \
            /opt/homebrew/bin/python3.12 \
            /usr/local/opt/python@3.12/bin/python3.12 \
            /usr/local/bin/python3.12
        do
            if _python_ok "$p"; then PYTHON="$p"; break; fi
        done
        [ -z "$PYTHON" ] && _python_ok python3.12 && PYTHON="python3.12" || true
        [ -z "$PYTHON" ] && _python_ok python3    && PYTHON="python3"    || true
    else
        echo "   -->  Homebrew khong co -- tai Python 3.12 tu python.org..."
        PY_PKG_URL="https://www.python.org/ftp/python/3.12.9/python-3.12.9-macos11.pkg"
        PY_PKG_TMP="/tmp/python_install.pkg"
        if curl -fL --max-time 300 --progress-bar "$PY_PKG_URL" -o "$PY_PKG_TMP" 2>&1; then
            echo "   -->  Dang cai (co the yeu cau mat khau Mac)..."
            sudo installer -pkg "$PY_PKG_TMP" -target / 2>&1 | grep -v "^$" || true
            rm -f "$PY_PKG_TMP"
            for p in /usr/local/bin/python3.12 \
                     /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12; do
                if _python_ok "$p"; then PYTHON="$p"; break; fi
            done
            [ -z "$PYTHON" ] && _python_ok python3.12 && PYTHON="python3.12" || true
        else
            rm -f "$PY_PKG_TMP"
        fi
    fi
    # Python tu python.org can chay Install Certificates de khoi loi SSL
    CERT_CMD="/Applications/Python 3.12/Install Certificates.command"
    [ -f "$CERT_CMD" ] && bash "$CERT_CMD" > /dev/null 2>&1 || true
fi

if [ -z "$PYTHON" ]; then
    echo ""
    echo " [LOI]  Khong tim thay va khong the tu dong cai Python 3.10+."
    echo ""
    echo "  CACH CAI PYTHON THU CONG:"
    echo "    Cach 1: Homebrew   -> brew install python@3.12"
    echo "    Cach 2: python.org -> https://www.python.org/downloads/"
    echo "            Tai 'Python 3.12.x macOS installer', bam Continue -> Install"
    echo ""
    open "https://www.python.org/downloads/" 2>/dev/null || true
    echo "  Cai xong, chay lai: bash macos_install.sh"
    echo "  Nhan Enter de dong..."
    read -r || true
    exit 1
fi

PY_VER="$("$PYTHON" --version 2>&1)"
echo "  [OK]  $PY_VER"
echo ""

# -- pip: bootstrap neu thieu (ensurepip -> get-pip.py) ----------------------
"$PYTHON" -m pip --version > /dev/null 2>&1 || {
    echo "   -->  Bootstrapping pip..."
    "$PYTHON" -m ensurepip --upgrade > /dev/null 2>&1 || \
        curl -sS https://bootstrap.pypa.io/get-pip.py | "$PYTHON"
}

# ============================================================
# BUOC 2: Kiem tra file khoa hoc
# ============================================================
echo "  [2/5] Kiem tra file khoa hoc..."
line
for f in requirements.txt common.py setup_key.py sales.csv \
         hello_agent.py lab1_persona.py lab2_one_tool.py lab3_full_agent.py; do
    [ -f "$f" ] || fail_exit "Thieu file $f." "Hay giai nen DAY DU goi khoa hoc roi chay lai."
done
echo "  [OK]  Du file."
echo ""

# ============================================================
# BUOC 3: Tao / kiem tra moi truong ao (.venv)
# ============================================================
echo "  [3/5] Tao / kiem tra moi truong ao..."
line

create_venv() {
    if ! "$PYTHON" -m venv "$VENV" 2>/dev/null; then
        echo "   -->  venv that bai, thu cai virtualenv..."
        "$PYTHON" -m pip install --quiet virtualenv
        "$PYTHON" -m virtualenv "$VENV"
    fi
}

if [ -f "$VENV/bin/python" ]; then
    echo "  [OK]  Da co san."
elif [ -d "$VENV" ]; then
    echo "   [!]  Moi truong ao bi hong -- dang xoa de tao lai..."
    rm -rf "$VENV"
    echo "   -->  Dang tao (chi lam mot lan)..."
    create_venv
    echo "  [OK]  Da tao xong."
else
    echo "   -->  Dang tao (chi lam mot lan)..."
    create_venv
    echo "  [OK]  Da tao xong."
fi

[ -f "$VENV/bin/python" ] || fail_exit "Khong the tao moi truong ao tai: $VENV" \
    "Kiem tra o dia con trong (can >= 300 MB). Thu xoa thu muc .venv/ roi chay lai."

PYV="$VENV/bin/python"
echo ""

# ============================================================
# BUOC 4: Cai dat / kiem tra thu vien
# ============================================================
echo "  [4/5] Cai dat / kiem tra thu vien..."
line

# Fast path: da import duoc thi bo qua (chay lai lan 2 khong can mang)
if "$PYV" -c "from google import genai; import dotenv" 2>/dev/null; then
    echo "  [OK]  Da co san."
else
    # Chi kiem tra Internet khi thuc su can cai
    if ! "$PYV" -c "import urllib.request as u; u.urlopen('https://pypi.org', timeout=8)" 2>/dev/null; then
        fail_exit "Khong ket noi duoc Internet (pypi.org)." \
                  "Kiem tra Wi-Fi / mang cong ty roi chay lai."
    fi
    echo "   -->  Dang cai (lan dau mat 1-2 phut, KHONG TAT cua so nay)..."
    "$PYV" -m pip install --upgrade pip --quiet > /dev/null 2>&1
    if ! "$PYV" -m pip install -r "$REQUIREMENTS" --quiet; then
        echo ""
        echo "  --- Chay lai lan cuoi de hien chi tiet loi ---"
        "$PYV" -m pip install -r "$REQUIREMENTS"
        fail_exit "Cai dat thu vien that bai." \
                  "Kiem tra mang / o dia. Thu xoa thu muc .venv/ roi chay lai."
    fi
    "$PYV" -c "from google import genai; import dotenv" 2>/dev/null || \
        fail_exit "Thu vien cai xong nhung khong import duoc." "Xoa thu muc .venv/ roi chay lai."
    echo "  [OK]  Cai dat xong."
fi
echo ""

# ============================================================
# BUOC 5: Gemini API key
# ============================================================
echo "  [5/5] Thiet lap Gemini API key..."
line

if [ -f ".env" ] && grep -q "GEMINI_API_KEY=." ".env" 2>/dev/null; then
    echo "  [OK]  Da co key trong .env, giu nguyen."
    echo "        (Doi key: chay bash run_macos.sh, chon muc 5)"
else
    echo ""
    echo "  Lay key MIEN PHI tai: https://aistudio.google.com/apikey"
    echo "  (dang nhap Google -> Create API key -> copy chuoi AIza...)"
    echo ""
    printf "  Dan key vao day roi Enter (hoac Enter de BO QUA, nhap sau tren web): "
    read -r USER_KEY || USER_KEY=""
    USER_KEY="$(echo "$USER_KEY" | tr -d '[:space:]')"
    if [ -n "$USER_KEY" ]; then
        echo "   -->  Dang kiem tra key voi Gemini..."
        if "$PYV" - "$USER_KEY" << 'PYEOF'
import sys
from setup_key import validate_key, save_key
ok, err = validate_key(sys.argv[1])
if ok:
    save_key(sys.argv[1])
    print("  [OK]  Key hop le, da luu vao .env")
    sys.exit(0)
print("   [!]  Key KHONG hop le:", err)
sys.exit(1)
PYEOF
        then :; else
            echo "   -->  Khong sao. Khi chay lab, trang web nhap key se tu mo."
        fi
    else
        echo "   -->  Bo qua. Khi chay lab lan dau, trang web nhap key se tu mo."
    fi
fi

echo ""
echo "  +--------------------------------------------------+"
echo "  |  HOAN TAT! Cach chay:   bash run_macos.sh        |"
echo "  |  (menu se hien ra de ban chon lab)               |"
echo "  +--------------------------------------------------+"
echo ""
echo "  Nhan Enter de dong..."
read -r || true
