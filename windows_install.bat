@echo off
REM ============================================================
REM windows_install.bat - Cai dat Business Analyst Agent (Windows)
REM Cach chay: nhay dup chuot vao file nay
REM ============================================================
REM -- Trick: cmd /k dam bao cua so KHONG BAO GIO tu dong dong --
if not defined _RELAUNCHED (
    set _RELAUNCHED=1
    cmd /k "%~f0" %*
    exit /b
)

chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Cai dat Business Analyst Agent

echo.
echo  +--------------------------------------------------+
echo  ^|  CAI DAT BUSINESS ANALYST AGENT  --  Windows     ^|
echo  +--------------------------------------------------+
echo.

set PYTHON=
set VENV=%~dp0.venv

:: ============================================================
:: BUOC 1: Tim Python 3.10+ (tu dong cai neu khong tim thay)
:: ============================================================
echo  [1/5] Tim Python 3.10+...
echo  ------------------------------------------------

REM 1a: Cac lenh co san trong PATH
for %%P in (python3.13 python3.12 python3.11 python3.10 python3 python) do (
    if "!PYTHON!" == "" (
        where %%P >nul 2>&1
        if not errorlevel 1 (
            %%P -c "import sys;sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
            if not errorlevel 1 set PYTHON=%%P
        )
    )
)

REM 1b: Duong dan cai dat mac dinh (PATH chua cap nhat sau khi cai moi)
if "!PYTHON!" == "" (
    for %%D in (
        "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "%ProgramFiles%\Python313\python.exe"
        "%ProgramFiles%\Python312\python.exe"
        "%ProgramFiles%\Python311\python.exe"
        "%ProgramFiles%\Python310\python.exe"
        "%ProgramFiles(x86)%\Python313\python.exe"
        "%ProgramFiles(x86)%\Python312\python.exe"
        "%ProgramFiles(x86)%\Python311\python.exe"
        "%ProgramFiles(x86)%\Python310\python.exe"
        "C:\Python313\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
        "C:\Python310\python.exe"
    ) do (
        if "!PYTHON!" == "" (
            if exist %%D (
                %%D -c "import sys;sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
                if not errorlevel 1 set PYTHON=%%D
            )
        )
    )
)

REM 1c: py.exe launcher -- lay duong dan python.exe thuc su
if "!PYTHON!" == "" (
    where py >nul 2>&1
    if not errorlevel 1 (
        for %%V in (3.13 3.12 3.11 3.10) do (
            if "!PYTHON!" == "" (
                for /f "tokens=*" %%P in ('py -%%V -c "import sys;print(sys.executable)" 2^>nul') do (
                    if "!PYTHON!" == "" (
                        "%%P" -c "import sys;sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
                        if not errorlevel 1 set PYTHON=%%P
                    )
                )
            )
        )
    )
)

REM -- Tu dong cai Python 3.12 neu van chua tim thay --
if "!PYTHON!" == "" (
    echo        Chua tim thay -- dang tu dong cai Python 3.12...

    REM Xac dinh kien truc CPU (amd64 hoac arm64)
    set PY_ARCH=amd64
    if "%PROCESSOR_ARCHITECTURE%"=="ARM64" set PY_ARCH=arm64

    REM Cach A: winget (co san tren Windows 10 1709+ va Windows 11)
    where winget >nul 2>&1
    if not errorlevel 1 (
        echo        Dung winget de cai Python 3.12...
        winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
        for %%D in (
            "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
            "%ProgramFiles%\Python312\python.exe"
            "C:\Python312\python.exe"
        ) do (
            if "!PYTHON!" == "" (
                if exist %%D (
                    %%D -c "import sys;sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
                    if not errorlevel 1 set PYTHON=%%D
                )
            )
        )
        if "!PYTHON!" == "" (
            where py >nul 2>&1
            if not errorlevel 1 (
                for /f "tokens=*" %%P in ('py -3.12 -c "import sys;print(sys.executable)" 2^>nul') do (
                    if "!PYTHON!" == "" set PYTHON=%%P
                )
                if "!PYTHON!" == "" (
                    for /f "tokens=*" %%P in ('py -3 -c "import sys;print(sys.executable)" 2^>nul') do (
                        if "!PYTHON!" == "" set PYTHON=%%P
                    )
                )
            )
        )
    ) else (
        REM Cach B: Tai file cai dat .exe qua PowerShell
        echo        winget khong co -- dang tai Python 3.12 tu python.org...
        set PY_VER_DL=3.12.9
        set PY_URL=https://www.python.org/ftp/python/!PY_VER_DL!/python-!PY_VER_DL!-!PY_ARCH!.exe
        echo        URL: !PY_URL!
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12;try{Invoke-WebRequest '!PY_URL!' -OutFile '%TEMP%\python_setup.exe' -UseBasicParsing;exit 0}catch{exit 1}"
        REM Kiem tra file hop le: phai lon hon 5 MB (tranh luu trang loi HTML)
        set DL_OK=0
        if exist "%TEMP%\python_setup.exe" (
            for %%S in ("%TEMP%\python_setup.exe") do (
                if %%~zS GTR 5000000 set DL_OK=1
            )
        )
        if "!DL_OK!" == "1" (
            echo        Dang cai dat Python 3.12 ^(chi nguoi dung hien tai, khong can Admin^)...
            "%TEMP%\python_setup.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
            del /f "%TEMP%\python_setup.exe" >nul 2>&1
            for %%D in (
                "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
                "%ProgramFiles%\Python312\python.exe"
                "C:\Python312\python.exe"
            ) do (
                if "!PYTHON!" == "" (
                    if exist %%D (
                        %%D -c "import sys;sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
                        if not errorlevel 1 set PYTHON=%%D
                    )
                )
            )
            if "!PYTHON!" == "" (
                where py >nul 2>&1
                if not errorlevel 1 (
                    for /f "tokens=*" %%P in ('py -3.12 -c "import sys;print(sys.executable)" 2^>nul') do (
                        if "!PYTHON!" == "" set PYTHON=%%P
                    )
                )
            )
        ) else (
            if exist "%TEMP%\python_setup.exe" del /f "%TEMP%\python_setup.exe" >nul 2>&1
            echo        Tai that bai hoac file khong hop le.
        )
    )
)

if "!PYTHON!" == "" (
    echo.
    echo  [LOI] Khong tim thay va khong the tu dong cai Python.
    echo.
    echo  CAI PYTHON THU CONG:
    echo    1. Vao: https://www.python.org/downloads/
    echo    2. Click "Download Python 3.12.x"
    echo    3. Mo file .exe vua tai
    echo    4. QUAN TRONG: Tick "Add Python to PATH" ^(o DUOI CUNG^)
    echo    5. Bam Install Now -- sau do chay lai windows_install.bat
    echo.
    echo  Neu da cai ma van loi:
    echo    Settings ^> Apps ^> Advanced app settings ^> App execution aliases
    echo    Tim python.exe va python3.exe -^> Tat OFF -^> Chay lai
    echo.
    start "" "https://www.python.org/downloads/"
    goto :end
)

for /f "tokens=*" %%V in ('"!PYTHON!" --version 2^>^&1') do set PY_VER=%%V
echo        OK - !PY_VER!
echo.

REM -- pip: bootstrap neu thieu (ensurepip -> get-pip.py) --
"!PYTHON!" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo        Bootstrapping pip...
    "!PYTHON!" -m ensurepip --upgrade >nul 2>&1
    if errorlevel 1 (
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12;try{Invoke-WebRequest 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%TEMP%\get-pip.py' -UseBasicParsing}catch{exit 1}"
        if exist "%TEMP%\get-pip.py" (
            "!PYTHON!" "%TEMP%\get-pip.py" --quiet
            del /f "%TEMP%\get-pip.py" >nul 2>&1
        )
    )
)

:: ============================================================
:: BUOC 2: Kiem tra file khoa hoc
:: ============================================================
echo  [2/5] Kiem tra file khoa hoc...
echo  ------------------------------------------------
for %%f in (requirements.txt common.py setup_key.py sales.csv hello_agent.py lab1_persona.py lab2_one_tool.py lab3_full_agent.py) do (
    if not exist "%%f" (
        echo  [LOI] Thieu file %%f
        echo        Hay giai nen DAY DU goi khoa hoc roi chay lai.
        goto :end
    )
)
echo        OK - du file
echo.

:: ============================================================
:: BUOC 3: Tao / kiem tra moi truong ao (.venv)
:: ============================================================
echo  [3/5] Tao / kiem tra moi truong ao...
echo  ------------------------------------------------

if exist "!VENV!\Scripts\python.exe" (
    echo        OK - da co san
    goto :venv_ok
)

REM Venv ton tai nhung thieu python.exe -> bi hong, xoa tao lai
if exist "!VENV!\" (
    echo        Phat hien venv bi hong -- dang xoa de tao lai...
    rmdir /s /q "!VENV!" 2>nul
)

echo        Dang tao ^(chi lam mot lan^)...
"!PYTHON!" -m venv "!VENV!" 2>nul
if errorlevel 1 (
    echo        venv that bai, thu cai virtualenv...
    "!PYTHON!" -m pip install virtualenv --quiet
    "!PYTHON!" -m virtualenv "!VENV!"
)

if not exist "!VENV!\Scripts\python.exe" (
    echo.
    echo  [LOI] Khong the tao moi truong ao tai: !VENV!
    echo  - Kiem tra o dia con trong ^(can ^>= 300 MB^)
    echo  - Thu xoa thu muc .venv\ roi chay lai
    goto :end
)
echo        OK - da tao xong

:venv_ok
set PYV=!VENV!\Scripts\python.exe
echo.

:: ============================================================
:: BUOC 4: Cai dat / kiem tra thu vien
:: ============================================================
echo  [4/5] Cai dat / kiem tra thu vien...
echo  ------------------------------------------------

REM Fast path: da import duoc thi bo qua (chay lai lan 2 khong can mang)
"!PYV!" -c "from google import genai; import dotenv" >nul 2>&1
if not errorlevel 1 (
    echo        OK - da co san
    goto :packages_ok
)

REM Chi kiem tra Internet khi thuc su can cai
"!PYV!" -c "import urllib.request as u;u.urlopen('https://pypi.org',timeout=8)" >nul 2>&1
if errorlevel 1 (
    echo  [LOI] Khong ket noi duoc Internet ^(pypi.org^).
    echo        Kiem tra Wi-Fi / mang cong ty roi chay lai.
    goto :end
)

echo        Dang cai ^(lan dau mat 1-2 phut -- KHONG TAT cua so nay^)...
"!PYV!" -m pip install --upgrade pip --quiet >nul 2>&1
"!PYV!" -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo  --- Chay lai lan cuoi de hien chi tiet loi ---
    "!PYV!" -m pip install -r requirements.txt
    echo.
    echo  [LOI] Cai dat thu vien that bai.
    echo  - Kiem tra ket noi internet / o dia
    echo  - Thu xoa thu muc .venv\ roi chay lai
    goto :end
)
"!PYV!" -c "from google import genai; import dotenv" >nul 2>&1
if errorlevel 1 (
    echo  [LOI] Thu vien cai xong nhung khong import duoc.
    echo        Xoa thu muc .venv\ roi chay lai file nay.
    goto :end
)
echo        OK - cai dat xong

:packages_ok
echo.

:: ============================================================
:: BUOC 5: Gemini API key
:: ============================================================
echo  [5/5] Thiet lap Gemini API key...
echo  ------------------------------------------------

set "HASKEY="
if exist ".env" (
    findstr /r "GEMINI_API_KEY=." ".env" >nul 2>&1 && set "HASKEY=1"
)
if defined HASKEY (
    echo        OK - da co key trong .env, giu nguyen.
    echo        ^(Doi key: chay run_windows.bat, chon muc 5^)
    goto :done_key
)

echo.
echo        Lay key MIEN PHI tai: https://aistudio.google.com/apikey
echo        ^(dang nhap Google - Create API key - copy chuoi AIza...^)
echo.
set "USER_KEY="
set /p USER_KEY="       Dan key vao day roi Enter (hoac Enter de BO QUA, nhap sau tren web): "
if "!USER_KEY!"=="" (
    echo        Bo qua. Khi chay lab lan dau, trang web nhap key se tu mo.
    goto :done_key
)
echo        Dang kiem tra key voi Gemini...
"!PYV!" -c "import sys; from setup_key import validate_key, save_key; ok, err = validate_key(sys.argv[1]); print('       OK - key hop le, da luu vao .env' if ok else '       Key KHONG hop le: ' + err); sys.exit(0 if ok else 1)" "!USER_KEY!"
if errorlevel 1 (
    echo        Khong sao. Khi ban chay lab, trang web nhap key se tu mo.
)
:done_key

echo.
echo  +--------------------------------------------------+
echo  ^|  HOAN TAT! Cach chay: nhay dup run_windows.bat   ^|
echo  ^|  (menu se hien ra de ban chon lab)               ^|
echo  +--------------------------------------------------+
echo.

:end
echo.
echo  Co the dong cua so nay.
endlocal
