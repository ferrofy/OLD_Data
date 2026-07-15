#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shellapi.h>
#include "../Core/App_Config.H"
#include "../Core/Shared_State.H"
#include "../Startup/Startup_Manager.H"
#include "Tray_Manager.H"

#pragma comment(lib, "shell32.lib")

static NOTIFYICONDATAW G_Nid   = {};
static HWND            G_Overlay_Hwnd = nullptr;
static HICON           G_Tray_Icon    = nullptr;

static HICON Create_Network_Icon()
{
    const int Sz = 16;
    HDC Screen_DC = GetDC(nullptr);
    HDC Mem_DC    = CreateCompatibleDC(Screen_DC);

    BITMAPINFOHEADER Bmi = {};
    Bmi.biSize     = sizeof(Bmi);
    Bmi.biWidth    = Sz;
    Bmi.biHeight   = -Sz;
    Bmi.biPlanes   = 1;
    Bmi.biBitCount = 32;
    Bmi.biCompression = BI_RGB;

    VOID* Bits = nullptr;
    HBITMAP Color_Bmp = CreateDIBSection(Mem_DC, (BITMAPINFO*)&Bmi, DIB_RGB_COLORS, &Bits, nullptr, 0);
    HBITMAP Mask_Bmp  = CreateBitmap(Sz, Sz, 1, 1, nullptr);

    SelectObject(Mem_DC, Color_Bmp);
    SetBkMode(Mem_DC, TRANSPARENT);

    HBRUSH Bg_Brush = CreateSolidBrush(RGB(10, 12, 18));
    RECT   R = {0, 0, Sz, Sz};
    FillRect(Mem_DC, &R, Bg_Brush);
    DeleteObject(Bg_Brush);

    HPEN Up_Pen  = CreatePen(PS_SOLID, 2, RGB(60, 200, 120));
    HPEN Dn_Pen  = CreatePen(PS_SOLID, 2, RGB(60, 140, 255));
    HPEN Old_Pen = (HPEN)SelectObject(Mem_DC, Up_Pen);

    MoveToEx(Mem_DC, 4, 10, nullptr);  LineTo(Mem_DC, 8,  3);
    MoveToEx(Mem_DC, 8,  3, nullptr);  LineTo(Mem_DC, 12, 10);

    SelectObject(Mem_DC, Dn_Pen);
    MoveToEx(Mem_DC, 4,  6, nullptr);  LineTo(Mem_DC, 8, 13);
    MoveToEx(Mem_DC, 8, 13, nullptr);  LineTo(Mem_DC, 12, 6);

    SelectObject(Mem_DC, Old_Pen);
    DeleteObject(Up_Pen);
    DeleteObject(Dn_Pen);

    ICONINFO Ii = {};
    Ii.fIcon    = TRUE;
    Ii.hbmColor = Color_Bmp;
    Ii.hbmMask  = Mask_Bmp;

    HICON Icon = CreateIconIndirect(&Ii);

    DeleteObject(Color_Bmp);
    DeleteObject(Mask_Bmp);
    DeleteDC(Mem_DC);
    ReleaseDC(nullptr, Screen_DC);

    return Icon;
}

bool Tray_Create(HWND Overlay_Hwnd)
{
    G_Overlay_Hwnd = Overlay_Hwnd;
    G_Tray_Icon    = Create_Network_Icon();

    ZeroMemory(&G_Nid, sizeof(G_Nid));
    G_Nid.cbSize           = sizeof(G_Nid);
    G_Nid.hWnd             = Overlay_Hwnd;
    G_Nid.uID              = TRAY_UID;
    G_Nid.uFlags           = NIF_ICON | NIF_MESSAGE | NIF_TIP;
    G_Nid.uCallbackMessage = WM_TRAY_ICON;
    G_Nid.hIcon            = G_Tray_Icon;
    wcscpy(G_Nid.szTip, L"Network Bar");

    return Shell_NotifyIconW(NIM_ADD, &G_Nid) == TRUE;
}

void Tray_Destroy()
{
    Shell_NotifyIconW(NIM_DELETE, &G_Nid);
    if (G_Tray_Icon) {
        DestroyIcon(G_Tray_Icon);
        G_Tray_Icon = nullptr;
    }
}

void Tray_Update_Tip(const wchar_t* Tip)
{
    if (!Tip) return;
    wcscpy(G_Nid.szTip, Tip);
    G_Nid.uFlags = NIF_TIP;
    Shell_NotifyIconW(NIM_MODIFY, &G_Nid);
}

static void Show_Tray_Menu(HWND Hwnd)
{
    HMENU Menu = CreatePopupMenu();
    if (!Menu) return;

    bool Visible  = G_App_State.Overlay_Visible.load(std::memory_order_relaxed);
    bool Startup  = Startup_Is_Enabled();
    G_App_State.Startup_Enabled.store(Startup, std::memory_order_relaxed);

    AppendMenuW(Menu, MF_STRING, IDM_OPEN,    L"Open Overlay");
    AppendMenuW(Menu, MF_SEPARATOR, 0,         nullptr);

    if (Visible) {
        AppendMenuW(Menu, MF_STRING, IDM_HIDE, L"Hide Overlay");
        AppendMenuW(Menu, MF_STRING | MF_GRAYED, IDM_SHOW, L"Show Overlay");
    } else {
        AppendMenuW(Menu, MF_STRING | MF_GRAYED, IDM_HIDE, L"Hide Overlay");
        AppendMenuW(Menu, MF_STRING, IDM_SHOW, L"Show Overlay");
    }

    AppendMenuW(Menu, MF_SEPARATOR, 0, nullptr);
    AppendMenuW(Menu, MF_STRING | (Startup ? MF_CHECKED : 0), IDM_STARTUP, L"Start With Windows");
    AppendMenuW(Menu, MF_SEPARATOR, 0, nullptr);
    AppendMenuW(Menu, MF_STRING, IDM_EXIT, L"Close App");

    POINT Pt;
    GetCursorPos(&Pt);
    SetForegroundWindow(Hwnd);
    TrackPopupMenu(Menu, TPM_BOTTOMALIGN | TPM_LEFTALIGN, Pt.x, Pt.y, 0, Hwnd, nullptr);
    PostMessage(Hwnd, WM_NULL, 0, 0);
    DestroyMenu(Menu);
}

void Tray_Handle_Message(HWND Hwnd, LPARAM LParam)
{
    switch (LOWORD(LParam)) {
        case WM_RBUTTONUP:
        case WM_CONTEXTMENU:
            Show_Tray_Menu(Hwnd);
            break;
        case WM_LBUTTONDBLCLK:
            if (!G_App_State.Overlay_Visible.load(std::memory_order_relaxed)) {
                G_App_State.Overlay_Visible.store(true, std::memory_order_relaxed);
                ShowWindow(G_Overlay_Hwnd, SW_SHOW);
                SetWindowPos(G_Overlay_Hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);
            }
            break;
    }
}
