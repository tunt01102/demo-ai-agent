@echo off
rem run_windows.bat - Menu chay cac lab (Windows)
rem Cach chay: nhay dup chuot vao file nay
cd /d "%~dp0"
title Business Analyst Agent

if not exist ".venv\Scripts\python.exe" (
    echo Chua cai dat. Hay chay truoc file: windows_install.bat
    pause
    exit /b 1
)
set "PYV=.venv\Scripts\python.exe"

:menu
echo.
echo ==============================================
echo  BUSINESS ANALYST AGENT - MENU
echo ==============================================
echo   1. Kiem tra ket noi (hello_agent)
echo   2. Lab 1 - Agent voi ban mo ta cong viec
echo   3. Lab 2 - Agent doc du lieu ban hang
echo   4. Lab 3 - Business Analyst Agent day du
echo   5. Nhap / doi API key
echo   0. Thoat
echo ==============================================
set "choice="
set /p choice="Chon so: "
if "%choice%"=="1" "%PYV%" hello_agent.py
if "%choice%"=="2" "%PYV%" lab1_persona.py
if "%choice%"=="3" "%PYV%" lab2_one_tool.py
if "%choice%"=="4" "%PYV%" lab3_full_agent.py
if "%choice%"=="5" "%PYV%" setup_key.py
if "%choice%"=="0" exit /b 0
goto :menu
