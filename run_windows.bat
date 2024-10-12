@echo off
cmdow @ /HID
setlocal enabledelayedexpansion
title Bu Ekrani Kapatmayiniz Aksi Takdirde Program Calismayi Durduracaktir
rem Python yüklü dizinleri bul
set "python_version="

rem where python ile kontrol et
for /f "tokens=*" %%i in ('where python') do (
    for /f "tokens=2 delims= " %%j in ('"%%i" --version') do (
        echo Found Python version: %%j
        if "%%j"=="3.10" (
            set "python_version=%%i"
        )
    )
)

rem py -3.10 ile kontrol et
if not defined python_version (
    for /f "tokens=*" %%i in ('py -3.10 --version 2^>nul') do (
        echo Found Python version: 3.10
        set "python_version=py -3.10"
    )
)

if defined python_version (
    echo Running Python 3.10 from: !python_version!

    rem requirements.txt dosyasının varlığını kontrol et
    if exist requirements.txt (
        echo Checking and installing missing packages from requirements.txt...

        rem Kütüphaneleri yükle
        cmd /c "!python_version! -m pip install -r requirements.txt"
    ) else (
        echo requirements.txt file not found.
    )

    rem CircuitMacropy.py dosyasının varlığını kontrol et
    if exist CircuitMacropy.py (
        echo Running CircuitMacropy.py...
        cmd /c "!python_version! -B CircuitMacropy.py"
    )

) else (
    echo Python 3.10 not found on this system.
    pause
)

endlocal
