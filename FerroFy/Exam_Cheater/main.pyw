import pyautogui
import time

Text_To_Type = """#include <windows.h>

LRESULT CALLBACK WindowProcedure(HWND Window_Handle, UINT Message, WPARAM Wparam, LPARAM Lparam)
{
    switch (Message)
    {
    case WM_COMMAND:
        MessageBox(NULL, "Button Clicked!", "Event", MB_OK);
        break;

    case WM_DESTROY:
        PostQuitMessage(0);
        break;

    default:
        return DefWindowProc(Window_Handle, Message, Wparam, Lparam);
    }

    return 0;
}

int WINAPI WinMain(HINSTANCE Instance_Handle, HINSTANCE Prev_Instance, LPSTR Args, int Show_Command)
{
    WNDCLASS Window_Class = {0};

    Window_Class.lpfnWndProc = WindowProcedure;
    Window_Class.hInstance = Instance_Handle;
    Window_Class.lpszClassName = "MyWindowClass";

    RegisterClass(&Window_Class);

    HWND Window_Handle = CreateWindow(
        "MyWindowClass",
        "VPX GUI App",
        WS_OVERLAPPEDWINDOW,
        100,
        100,
        500,
        300,
        NULL,
        NULL,
        Instance_Handle,
        NULL);

    CreateWindow(
        "BUTTON",
        "Click Me",
        WS_VISIBLE | WS_CHILD,
        180,
        100,
        120,
        40,
        Window_Handle,
        NULL,
        Instance_Handle,
        NULL);

    ShowWindow(Window_Handle, Show_Command);

    MSG Message;

    while (GetMessage(&Message, NULL, 0, 0))
    {
        TranslateMessage(&Message);
        DispatchMessage(&Message);
    }

    return 0;
}"""

Delay_Before_Start = 3

time.sleep(Delay_Before_Start)

for Char in Text_To_Type:
    pyautogui.write(Char)


# import keyboard

# while True:
#     if keyboard.is_pressed('x'):
#         print("abcd")
#         while keyboard.is_pressed('x'):
#             pass