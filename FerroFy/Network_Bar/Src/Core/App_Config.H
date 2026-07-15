#pragma once
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define APP_NAME            L"Network_Bar"
#define APP_CLASS           L"NetworkBarOverlay"
#define TRAY_CLASS          L"NetworkBarTray"
#define APP_VERSION         L"1.0.0"
#define APP_MUTEX           L"NetworkBar_SingleInstance_Mutex"

#define WM_TRAY_ICON        (WM_USER + 1)
#define TRAY_UID            1001

#define IDM_OPEN            2001
#define IDM_HIDE            2002
#define IDM_SHOW            2003
#define IDM_STARTUP         2004
#define IDM_EXIT            2005

#define OVERLAY_W           200
#define OVERLAY_H           120
#define OVERLAY_MARGIN_X    12
#define OVERLAY_MARGIN_Y    12
#define CORNER_RADIUS       10

#define NET_POLL_MS         500
#define UI_REFRESH_MS       500
#define PING_INTERVAL_MS    2000
#define PING_TIMEOUT_MS     1000

#define REG_RUN_KEY         L"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
#define REG_VALUE_NAME      APP_NAME

#define FONT_FAMILY         L"Segoe UI"
#define FONT_SIZE_LABEL     9
#define FONT_SIZE_VALUE     12

#define OVERLAY_ALPHA       210

#define CLR_BG              RGB(12,  14,  20)
#define CLR_ACCENT          RGB(0,   200, 150)
#define CLR_ACCENT2         RGB(60,  140, 255)
#define CLR_TEXT_PRIMARY    RGB(230, 235, 245)
#define CLR_TEXT_SECONDARY  RGB(120, 130, 150)
#define CLR_UP              RGB(60,  200, 120)
#define CLR_DOWN            RGB(60,  140, 255)
#define CLR_PING_GOOD       RGB(60,  200, 120)
#define CLR_PING_MED        RGB(255, 180, 40)
#define CLR_PING_BAD        RGB(255, 80,  80)
#define CLR_DIVIDER         RGB(35,  40,  55)