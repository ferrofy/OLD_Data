#pragma once
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

bool  Tray_Create(HWND Overlay_Hwnd);
void  Tray_Destroy();
void  Tray_Update_Tip(const wchar_t* Tip);
LRESULT CALLBACK Tray_WndProc(HWND Hwnd, UINT Msg, WPARAM WParam, LPARAM LParam);
