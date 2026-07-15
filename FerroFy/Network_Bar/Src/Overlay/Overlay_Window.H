#pragma once
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

bool  Overlay_Register_Class(HINSTANCE HInst);
HWND  Overlay_Create(HINSTANCE HInst);
void  Overlay_Render(HWND Hwnd);
LRESULT CALLBACK Overlay_WndProc(HWND Hwnd, UINT Msg, WPARAM WParam, LPARAM LParam);
