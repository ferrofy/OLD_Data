#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include "../Core/App_Config.H"
#include "Startup_Manager.H"

bool Startup_Is_Enabled()
{
    HKEY  Key;
    if (RegOpenKeyExW(HKEY_CURRENT_USER, REG_RUN_KEY, 0, KEY_READ, &Key) != ERROR_SUCCESS)
        return false;

    DWORD Type = 0, Size = 0;
    bool  Found = (RegQueryValueExW(Key, REG_VALUE_NAME, nullptr, &Type, nullptr, &Size) == ERROR_SUCCESS);
    RegCloseKey(Key);
    return Found;
}

void Startup_Set(bool Enable)
{
    HKEY Key;
    if (RegOpenKeyExW(HKEY_CURRENT_USER, REG_RUN_KEY, 0, KEY_WRITE, &Key) != ERROR_SUCCESS)
        return;

    if (Enable) {
        wchar_t Exe_Path[MAX_PATH] = {};
        GetModuleFileNameW(nullptr, Exe_Path, MAX_PATH);
        RegSetValueExW(Key, REG_VALUE_NAME, 0, REG_SZ,
            (const BYTE*)Exe_Path,
            (DWORD)((wcslen(Exe_Path) + 1) * sizeof(wchar_t)));
    } else {
        RegDeleteValueW(Key, REG_VALUE_NAME);
    }

    RegCloseKey(Key);
}
