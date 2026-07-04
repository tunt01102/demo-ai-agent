#!/bin/bash
# run_macos.sh - Menu chay cac lab (macOS)
# Cach chay: bash run_macos.sh
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "Chua cai dat. Hay chay truoc:  bash macos_install.sh"
  exit 1
fi
PYV=".venv/bin/python"

while true; do
  echo ""
  echo "=============================================="
  echo " BUSINESS ANALYST AGENT - MENU"
  echo "=============================================="
  echo "  1. Kiem tra ket noi (hello_agent)"
  echo "  2. Lab 1 - Agent voi ban mo ta cong viec"
  echo "  3. Lab 2 - Agent doc du lieu ban hang"
  echo "  4. Lab 3 - Business Analyst Agent day du"
  echo "  5. Nhap / doi API key"
  echo "  0. Thoat"
  echo "=============================================="
  printf "Chon so: "
  read -r choice
  case "$choice" in
    1) "$PYV" hello_agent.py ;;
    2) "$PYV" lab1_persona.py ;;
    3) "$PYV" lab2_one_tool.py ;;
    4) "$PYV" lab3_full_agent.py ;;
    5) "$PYV" setup_key.py ;;
    0) exit 0 ;;
    *) echo "Chon 0-5 thoi ban oi." ;;
  esac
done
