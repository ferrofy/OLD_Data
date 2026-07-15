#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shellapi.h>
#include <dwmapi.h>
#include <cstdio>
#include <cmath>
#include "../Core/App_Config.H"
#include "../Core/Shared_State.H"
#include "../Tray/Tray_Manager.H"
#include "../Startup/Startup_Manager.H"
#include "Overlay_Window.H"

#pragma comment(lib, "gdi32.lib")
#pragma comment(lib, "dwmapi.lib")
#pragma comment(lib, "user32.lib")

static HINSTANCE G_HInst     = nullptr;
static HFONT     G_Font_Label = nullptr;
static HFONT     G_Font_Value = nullptr;
static HFONT     G_Font_Title = nullptr;
static bool      G_Dragging   = false;
static POINT     G_Drag_Start = {};
static POINT     G_Win_Start  = {};

static void Format_Speed(double Bps, wchar_t* Buf, int Buf_Len)
{
    if (Bps >= 1024.0 * 1024.0 * 1024.0)
        swprintf(Buf, Buf_Len, L"%.2f GB/s", Bps / (1024.0 * 1024.0 * 1024.0));
    else if (Bps >= 1024.0 * 1024.0)
        swprintf(Buf, Buf_Len, L"%.2f MB/s", Bps / (1024.0 * 1024.0));
    else if (Bps >= 1024.0)
        swprintf(Buf, Buf_Len, L"%.1f KB/s", Bps / 1024.0);
    else
        swprintf(Buf, Buf_Len, L"%.0f B/s", Bps);
}

static void Format_Bytes(uint64_t Bytes, wchar_t* Buf, int Buf_Len)
{
    if (Bytes >= (uint64_t)1024 * 1024 * 1024)
        swprintf(Buf, Buf_Len, L"%.2f GB", (double)Bytes / (1024.0 * 1024.0 * 1024.0));
    else if (Bytes >= 1024 * 1024)
        swprintf(Buf, Buf_Len, L"%.1f MB", (double)Bytes / (1024.0 * 1024.0));
    else if (Bytes >= 1024)
        swprintf(Buf, Buf_Len, L"%.1f KB", (double)Bytes / 1024.0);
    else
        swprintf(Buf, Buf_Len, L"%llu B", (unsigned long long)Bytes);
}

static void Draw_Rounded_Rect(HDC Dc, RECT* R, int Radius, HBRUSH Brush)
{
    HRGN Rgn = CreateRoundRectRgn(R->left, R->top, R->right, R->bottom, Radius, Radius);
    FillRgn(Dc, Rgn, Brush);
    DeleteObject(Rgn);
}

static void Draw_Text_Row(HDC Dc, const wchar_t* Label, const wchar_t* Value, COLORREF Val_Color,
                           int X, int Y, int W)
{
    RECT Label_Rect = { X, Y, X + 80, Y + 18 };
    RECT Value_Rect = { X + 80, Y, X + W, Y + 18 };

    SelectObject(Dc, G_Font_Label);
    SetTextColor(Dc, CLR_TEXT_SECONDARY);
    DrawTextW(Dc, Label, -1, &Label_Rect, DT_LEFT | DT_VCENTER | DT_SINGLELINE);

    SelectObject(Dc, G_Font_Value);
    SetTextColor(Dc, Val_Color);
    DrawTextW(Dc, Value, -1, &Value_Rect, DT_RIGHT | DT_VCENTER | DT_SINGLELINE);
}

static void Draw_Divider(HDC Dc, int X, int Y, int W)
{
    HPEN Pen     = CreatePen(PS_SOLID, 1, CLR_DIVIDER);
    HPEN Old_Pen = (HPEN)SelectObject(Dc, Pen);
    MoveToEx(Dc, X, Y, nullptr);
    LineTo(Dc, X + W, Y);
    SelectObject(Dc, Old_Pen);
    DeleteObject(Pen);
}

static void Draw_Arrow(HDC Dc, int X, int Y, bool Up, COLORREF Color)
{
    HPEN Pen     = CreatePen(PS_SOLID, 2, Color);
    HPEN Old_Pen = (HPEN)SelectObject(Dc, Pen);
    if (Up) {
        MoveToEx(Dc, X,     Y + 7, nullptr);
        LineTo(Dc,   X + 5, Y);
        MoveToEx(Dc, X + 5, Y,     nullptr);
        LineTo(Dc,   X + 10, Y + 7);
        MoveToEx(Dc, X + 5, Y,     nullptr);
        LineTo(Dc,   X + 5, Y + 10);
    } else {
        MoveToEx(Dc, X,     Y + 3, nullptr);
        LineTo(Dc,   X + 5, Y + 10);
        MoveToEx(Dc, X + 5, Y + 10, nullptr);
        LineTo(Dc,   X + 10, Y + 3);
        MoveToEx(Dc, X + 5, Y,     nullptr);
        LineTo(Dc,   X + 5, Y + 10);
    }
    SelectObject(Dc, Old_Pen);
    DeleteObject(Pen);
}

static void Draw_Status_Dot(HDC Dc, int X, int Y, bool Online)
{
    HBRUSH Brush     = CreateSolidBrush(Online ? CLR_PING_GOOD : CLR_PING_BAD);
    HBRUSH Old_Brush = (HBRUSH)SelectObject(Dc, Brush);
    HPEN   Null_Pen  = (HPEN)SelectObject(Dc, GetStockObject(NULL_PEN));
    Ellipse(Dc, X, Y, X + 7, Y + 7);
    SelectObject(Dc, Old_Brush);
    SelectObject(Dc, Null_Pen);
    DeleteObject(Brush);
}

void Overlay_Render(HWND Hwnd)
{
    PAINTSTRUCT Ps;
    HDC Hdc = BeginPaint(Hwnd, &Ps);

    RECT Client;
    GetClientRect(Hwnd, &Client);
    int W = Client.right;
    int H = Client.bottom;

    HDC     Mem_Dc  = CreateCompatibleDC(Hdc);
    HBITMAP Bmp     = CreateCompatibleBitmap(Hdc, W, H);
    HBITMAP Old_Bmp = (HBITMAP)SelectObject(Mem_Dc, Bmp);

    SetBkMode(Mem_Dc, TRANSPARENT);

    HBRUSH Bg_Brush = CreateSolidBrush(CLR_BG);
    RECT   Bg_Rect  = {0, 0, W, H};
    Draw_Rounded_Rect(Mem_Dc, &Bg_Rect, CORNER_RADIUS, Bg_Brush);
    DeleteObject(Bg_Brush);

    HBRUSH Header_Brush = CreateSolidBrush(RGB(18, 22, 32));
    RECT   Header_Rect  = {0, 0, W, 24};
    FillRect(Mem_Dc, &Header_Rect, Header_Brush);
    DeleteObject(Header_Brush);

    double  Upload   = G_Net_Stats.Upload_Bps.load(std::memory_order_relaxed);
    double  Download = G_Net_Stats.Download_Bps.load(std::memory_order_relaxed);
    uint64_t Sent    = G_Net_Stats.Total_Sent.load(std::memory_order_relaxed);
    uint64_t Recv    = G_Net_Stats.Total_Recv.load(std::memory_order_relaxed);
    uint32_t Ping    = G_Net_Stats.Ping_Ms.load(std::memory_order_relaxed);
    bool     Online  = G_Net_Stats.Is_Online.load(std::memory_order_relaxed);

    SelectObject(Mem_Dc, G_Font_Title);
    SetTextColor(Mem_Dc, CLR_ACCENT);
    RECT Title_Rect = {12, 5, W - 30, 22};
    DrawTextW(Mem_Dc, L"NETWORK BAR", -1, &Title_Rect, DT_LEFT | DT_VCENTER | DT_SINGLELINE);

    Draw_Status_Dot(Mem_Dc, W - 20, 9, Online);

    Draw_Divider(Mem_Dc, 0, 24, W);

    int Pad  = 12;
    int Row_W = W - Pad * 2;
    int Y    = 32;

    wchar_t Up_Buf[32], Dn_Buf[32];
    Format_Speed(Upload,   Up_Buf, 32);
    Format_Speed(Download, Dn_Buf, 32);

    Draw_Arrow(Mem_Dc, Pad, Y + 2, true,  CLR_UP);
    Draw_Text_Row(Mem_Dc, L"Upload",   Up_Buf, CLR_UP,   Pad + 14, Y, Row_W - 14);

    Y += 20;
    Draw_Arrow(Mem_Dc, Pad, Y + 2, false, CLR_DOWN);
    Draw_Text_Row(Mem_Dc, L"Download", Dn_Buf, CLR_DOWN, Pad + 14, Y, Row_W - 14);

    Y += 22;
    Draw_Divider(Mem_Dc, Pad, Y, Row_W);
    Y += 6;

    wchar_t Sent_Buf[32], Recv_Buf[32];
    Format_Bytes(Sent, Sent_Buf, 32);
    Format_Bytes(Recv, Recv_Buf, 32);

    Draw_Text_Row(Mem_Dc, L"Sent",     Sent_Buf, CLR_TEXT_SECONDARY, Pad, Y, Row_W);
    Y += 18;
    Draw_Text_Row(Mem_Dc, L"Received", Recv_Buf, CLR_TEXT_SECONDARY, Pad, Y, Row_W);

    Y += 20;
    Draw_Divider(Mem_Dc, Pad, Y, Row_W);
    Y += 6;

    COLORREF Ping_Color = (Ping < 50) ? CLR_PING_GOOD : (Ping < 150) ? CLR_PING_MED : CLR_PING_BAD;
    wchar_t  Ping_Buf[32];
    if (Online)
        swprintf(Ping_Buf, 32, L"%u ms", Ping);
    else
        wcscpy(Ping_Buf, L"Offline");

    Draw_Text_Row(Mem_Dc, L"Ping",   Ping_Buf, Ping_Color, Pad, Y, Row_W);

    BitBlt(Hdc, 0, 0, W, H, Mem_Dc, 0, 0, SRCCOPY);

    SelectObject(Mem_Dc, Old_Bmp);
    DeleteObject(Bmp);
    DeleteDC(Mem_Dc);
    EndPaint(Hwnd, &Ps);
}

static void Ensure_Fonts()
{
    if (G_Font_Label) return;

    G_Font_Label = CreateFontW(
        -(FONT_SIZE_LABEL + 1), 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
        DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_SWISS, FONT_FAMILY);

    G_Font_Value = CreateFontW(
        -(FONT_SIZE_VALUE), 0, 0, 0, FW_SEMIBOLD, FALSE, FALSE, FALSE,
        DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_SWISS, FONT_FAMILY);

    G_Font_Title = CreateFontW(
        -9, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE,
        DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_SWISS, FONT_FAMILY);
}

extern void Tray_Handle_Message(HWND Hwnd, LPARAM LParam);

LRESULT CALLBACK Overlay_WndProc(HWND Hwnd, UINT Msg, WPARAM WParam, LPARAM LParam)
{
    switch (Msg) {
        case WM_CREATE:
            Ensure_Fonts();
            SetTimer(Hwnd, 1, UI_REFRESH_MS, nullptr);
            return 0;

        case WM_TIMER:
            if (WParam == 1) {
                InvalidateRect(Hwnd, nullptr, FALSE);

                bool    Online = G_Net_Stats.Is_Online.load(std::memory_order_relaxed);
                uint32_t Ping  = G_Net_Stats.Ping_Ms.load(std::memory_order_relaxed);
                wchar_t  Tip[128];
                if (Online)
                    swprintf(Tip, 128, L"Network Bar | Ping: %u ms", Ping);
                else
                    wcscpy(Tip, L"Network Bar | Offline");
                Tray_Update_Tip(Tip);
            }
            return 0;

        case WM_PAINT:
            Overlay_Render(Hwnd);
            return 0;

        case WM_ERASEBKGND:
            return 1;

        case WM_TRAY_ICON:
            Tray_Handle_Message(Hwnd, LParam);
            return 0;

        case WM_COMMAND:
            switch (LOWORD(WParam)) {
                case IDM_OPEN:
                case IDM_SHOW:
                    G_App_State.Overlay_Visible.store(true, std::memory_order_relaxed);
                    ShowWindow(Hwnd, SW_SHOW);
                    SetWindowPos(Hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);
                    break;
                case IDM_HIDE:
                    G_App_State.Overlay_Visible.store(false, std::memory_order_relaxed);
                    ShowWindow(Hwnd, SW_HIDE);
                    break;
                case IDM_STARTUP: {
                    bool Cur = Startup_Is_Enabled();
                    Startup_Set(!Cur);
                    G_App_State.Startup_Enabled.store(!Cur, std::memory_order_relaxed);
                    break;
                }
                case IDM_EXIT:
                    G_App_State.Running.store(false, std::memory_order_relaxed);
                    DestroyWindow(Hwnd);
                    break;
                case 3001: {
                    bool Cur = G_App_State.Draggable.load(std::memory_order_relaxed);
                    G_App_State.Draggable.store(!Cur, std::memory_order_relaxed);
                    break;
                }
            }
            return 0;

        case WM_LBUTTONDOWN:
            if (G_App_State.Draggable.load(std::memory_order_relaxed)) {
                G_Dragging = true;
                G_Drag_Start.x = LOWORD(LParam);
                G_Drag_Start.y = HIWORD(LParam);
                RECT Wr;
                GetWindowRect(Hwnd, &Wr);
                G_Win_Start.x = Wr.left;
                G_Win_Start.y = Wr.top;
                SetCapture(Hwnd);
            }
            return 0;

        case WM_MOUSEMOVE:
            if (G_Dragging) {
                int Dx = (int)(short)LOWORD(LParam) - G_Drag_Start.x;
                int Dy = (int)(short)HIWORD(LParam) - G_Drag_Start.y;
                SetWindowPos(Hwnd, HWND_TOPMOST,
                    G_Win_Start.x + Dx, G_Win_Start.y + Dy,
                    0, 0, SWP_NOSIZE);
                G_App_State.Overlay_X.store(G_Win_Start.x + Dx, std::memory_order_relaxed);
                G_App_State.Overlay_Y.store(G_Win_Start.y + Dy, std::memory_order_relaxed);
            }
            return 0;

        case WM_LBUTTONUP:
            if (G_Dragging) {
                G_Dragging = false;
                ReleaseCapture();
            }
            return 0;

        case WM_RBUTTONUP: {
            POINT Pt = { LOWORD(LParam), HIWORD(LParam) };
            ClientToScreen(Hwnd, &Pt);
            HMENU Menu = CreatePopupMenu();
            bool  Drag = G_App_State.Draggable.load(std::memory_order_relaxed);
            AppendMenuW(Menu, MF_STRING | (Drag ? MF_CHECKED : 0), 3001, L"Lock / Unlock Position");
            SetForegroundWindow(Hwnd);
            TrackPopupMenu(Menu, TPM_LEFTALIGN | TPM_TOPALIGN, Pt.x, Pt.y, 0, Hwnd, nullptr);
            PostMessage(Hwnd, WM_NULL, 0, 0);
            DestroyMenu(Menu);
            return 0;
        }

        case WM_DESTROY:
            KillTimer(Hwnd, 1);
            if (G_Font_Label) { DeleteObject(G_Font_Label); G_Font_Label = nullptr; }
            if (G_Font_Value) { DeleteObject(G_Font_Value); G_Font_Value = nullptr; }
            if (G_Font_Title) { DeleteObject(G_Font_Title); G_Font_Title = nullptr; }
            PostQuitMessage(0);
            return 0;

        default:
            break;
    }
    return DefWindowProcW(Hwnd, Msg, WParam, LParam);
}

bool Overlay_Register_Class(HINSTANCE HInst)
{
    G_HInst = HInst;

    WNDCLASSEXW Wc   = {};
    Wc.cbSize        = sizeof(Wc);
    Wc.lpfnWndProc   = Overlay_WndProc;
    Wc.hInstance     = HInst;
    Wc.hCursor       = LoadCursor(nullptr, IDC_ARROW);
    Wc.hbrBackground = nullptr;
    Wc.lpszClassName = APP_CLASS;
    Wc.style         = CS_HREDRAW | CS_VREDRAW;

    return RegisterClassExW(&Wc) != 0;
}

HWND Overlay_Create(HINSTANCE HInst)
{

    DWORD Ex_Style = WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE | WS_EX_LAYERED;
    DWORD Style    = WS_POPUP | WS_VISIBLE;

    HWND Hwnd = CreateWindowExW(
        Ex_Style, APP_CLASS, APP_NAME, Style,
        OVERLAY_MARGIN_X, OVERLAY_MARGIN_Y,
        OVERLAY_W, OVERLAY_H,
        nullptr, nullptr, HInst, nullptr);

    if (!Hwnd) return nullptr;

    SetLayeredWindowAttributes(Hwnd, 0, OVERLAY_ALPHA, LWA_ALPHA);

    BOOL Dark_Mode = TRUE;
    DwmSetWindowAttribute(Hwnd, 20, &Dark_Mode, sizeof(Dark_Mode));

    return Hwnd;
}
