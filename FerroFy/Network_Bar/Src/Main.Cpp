#define WIN32_LEAN_AND_MEAN
#define UNICODE
#define _UNICODE
#include <windows.h>
#include "Core/App_Config.H"
#include "Core/Shared_State.H"
#include "Network/Net_Monitor.H"
#include "Overlay/Overlay_Window.H"
#include "Tray/Tray_Manager.H"
#include "Startup/Startup_Manager.H"

#pragma comment(lib, "user32.lib")
#pragma comment(lib, "gdi32.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "dwmapi.lib")

int WINAPI wWinMain(HINSTANCE HInst, HINSTANCE, LPWSTR, int)
{
    HANDLE Mutex = CreateMutexW(nullptr, TRUE, APP_MUTEX);
    if (GetLastError() == ERROR_ALREADY_EXISTS) {
        if (Mutex) CloseHandle(Mutex);
        return 0;
    }

    G_App_State.Startup_Enabled.store(Startup_Is_Enabled(), std::memory_order_relaxed);

    if (!Overlay_Register_Class(HInst)) {
        CloseHandle(Mutex);
        return 1;
    }

    HWND Overlay_Hwnd = Overlay_Create(HInst);
    if (!Overlay_Hwnd) {
        CloseHandle(Mutex);
        return 1;
    }

    if (!Tray_Create(Overlay_Hwnd)) {
        DestroyWindow(Overlay_Hwnd);
        CloseHandle(Mutex);
        return 1;
    }

    if (!Net_Monitor_Start()) {
        Tray_Destroy();
        DestroyWindow(Overlay_Hwnd);
        CloseHandle(Mutex);
        return 1;
    }

    ShowWindow(Overlay_Hwnd, SW_SHOW);
    UpdateWindow(Overlay_Hwnd);

    MSG Msg;
    while (GetMessageW(&Msg, nullptr, 0, 0)) {
        TranslateMessage(&Msg);
        DispatchMessageW(&Msg);
    }

    G_App_State.Running.store(false, std::memory_order_relaxed);
    Net_Monitor_Stop();
    Tray_Destroy();

    if (Mutex) CloseHandle(Mutex);
    return (int)Msg.wParam;
}