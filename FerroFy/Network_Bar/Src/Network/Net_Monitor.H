#pragma once
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

bool  Net_Monitor_Start();
void  Net_Monitor_Stop();
DWORD WINAPI Net_Monitor_Thread(LPVOID Param);
