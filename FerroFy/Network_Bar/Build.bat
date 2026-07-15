@echo off
setlocal EnableDelayedExpansion

echo.
echo  ===================================
echo   Network_Bar - Build Script
echo   Using: MinGW64 (g++)
echo  ===================================
echo.

set GPP=C:\msys64\mingw64\bin\g++.exe

if not exist "%GPP%" (
    echo  [ERROR] g++ not found at %GPP%
    echo  Please install MSYS2 + MinGW64 or update GPP path in this script.
    pause
    exit /b 1
)

if not exist "Build" mkdir Build

set SRC=Src\Main.Cpp Src\Overlay\Overlay_Window.Cpp Src\Network\Net_Monitor.Cpp Src\Tray\Tray_Manager.Cpp Src\Startup\Startup_Manager.Cpp

set FLAGS=-O2 -std=c++17 -DUNICODE -D_UNICODE -DWIN32_LEAN_AND_MEAN -mwindows -municode

set LINKS=-liphlpapi -lws2_32 -lgdi32 -lshell32 -ldwmapi -ladvapi32 -luser32 -lkernel32 -liphlpapi -licmp

echo  [*] Compiling with g++...

"%GPP%" %FLAGS% %SRC% -o Build\Network_Bar.exe %LINKS%

if %errorlevel% equ 0 (
    echo.
    echo  [OK] Build Successful!
    echo  [>>] Output: Build\Network_Bar.exe
    echo.
) else (
    echo.
    echo  [FAIL] Build Failed - Check Errors Above.
    echo.
    pause
    exit /b 1
)

endlocal
