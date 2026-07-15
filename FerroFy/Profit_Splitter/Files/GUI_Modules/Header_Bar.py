import tkinter as Tk
from Files.GUI_Modules.Constants import (
    Bg_Panel, Bg_Card, Bg_Main, Border_Glow, Border_Color,
    Accent_Gold, Accent_Gold_Dark, Accent_Cyan, Accent_Purple,
    Glow_Gold, Font_Tab, Txt_Muted,
)
from Files.GUI_Modules.Utils import Bind_Hover

Nav_Glow_Colors = [
    Accent_Cyan,
    Accent_Purple,
    Accent_Gold,
    "#4ADE80",
    "#74C0FC",
    "#FFFFFF",
]

def Build_Header(Gui_Ref):
    Nav_Bar = Tk.Frame(Gui_Ref.Root, bg=Bg_Main, pady=10)
    Nav_Bar.pack(fill=Tk.X, padx=0)

    Tk.Frame(Nav_Bar, bg=Accent_Gold_Dark, height=2).pack(fill=Tk.X)

    Inner_Bar = Tk.Frame(Nav_Bar, bg=Bg_Main)
    Inner_Bar.pack(fill=Tk.X, padx=20, pady=(8, 4))

    Left_Nav = Tk.Frame(Inner_Bar, bg=Bg_Main)
    Left_Nav.pack(side=Tk.LEFT, fill=Tk.Y)

    Nav_Buttons = [
        ("📈  Graph",     Gui_Ref.Graph_View.Show,   Accent_Cyan),
        ("🥧  Pie Chart", Gui_Ref.Pie_View.Show,     Accent_Purple),
        ("📊  Summary",   Gui_Ref.Summary_View.Show, Accent_Gold),
        ("🎯  Goals",     Gui_Ref.Goal_View.Show,    "#4ADE80"),
        ("📋  History",   Gui_Ref.History_View.Show, "#74C0FC"),
        ("💾  Save",      Gui_Ref.Do_Save,           "#FFFFFF"),
    ]

    for Txt, Cmd, Clr in Nav_Buttons:
        Btn_Wrap = Tk.Frame(Left_Nav, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
        Btn_Wrap.pack(side=Tk.LEFT, padx=5)

        Btn = Tk.Button(
            Btn_Wrap,
            text=Txt,
            bg=Bg_Card,
            fg=Clr,
            font=Font_Tab,
            borderwidth=0,
            cursor="hand2",
            command=Cmd,
            activebackground=Glow_Gold,
            activeforeground=Accent_Gold,
        )
        Btn.pack(ipadx=16, ipady=9)
        Bind_Hover(Btn, Bg_Card, Border_Glow, Clr, Accent_Gold_Dark)

    Right_Nav = Tk.Frame(Inner_Bar, bg=Bg_Main)
    Right_Nav.pack(side=Tk.RIGHT, fill=Tk.Y)

    Tk.Label(Right_Nav, text="🕐", font=("Segoe UI", 13), bg=Bg_Main, fg=Accent_Cyan).pack(side=Tk.LEFT, padx=(0, 4), pady=6)
    Gui_Ref.Clock_Label = Tk.Label(Right_Nav, text="", font=("Segoe UI", 11), bg=Bg_Main, fg=Txt_Muted)
    Gui_Ref.Clock_Label.pack(side=Tk.LEFT, pady=6, padx=4)

    Sep2 = Tk.Frame(Gui_Ref.Root, bg=Border_Color, height=1)
    Sep2.pack(fill=Tk.X, padx=20)