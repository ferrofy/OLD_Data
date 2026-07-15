import tkinter as Tk
from Files.GUI_Modules.Constants import Bg_Panel, Accent_Gold, Border_Glow

def Bind_Hover(Widget, Bg_Normal, Bg_Hover, Fg_Normal="#FFFFFF", Fg_Hover="#000000"):
    def On_Enter(E):
        Widget.config(bg=Bg_Hover, fg=Fg_Hover)
    def On_Leave(E):
        Widget.config(bg=Bg_Normal, fg=Fg_Normal)
    Widget.bind("<Enter>", On_Enter)
    Widget.bind("<Leave>", On_Leave)

def Bind_Hover_Frame(Widget, Frame, Bg_Normal, Bg_Hover, Fg_Normal="#FFFFFF", Fg_Hover="#000000"):
    def On_Enter(E):
        Widget.config(bg=Bg_Hover, fg=Fg_Hover)
        Frame.config(bg=Bg_Hover)
    def On_Leave(E):
        Widget.config(bg=Bg_Normal, fg=Fg_Normal)
        Frame.config(bg=Bg_Normal)
    Widget.bind("<Enter>", On_Enter)
    Widget.bind("<Leave>", On_Leave)
    Frame.bind("<Enter>", On_Enter)
    Frame.bind("<Leave>", On_Leave)

def Create_Scrollable_Tab(Notebook, Text):
    Outer = Tk.Frame(Notebook, bg=Bg_Panel)
    Notebook.add(Outer, text=Text)

    Canvas = Tk.Canvas(Outer, bg=Bg_Panel, bd=0, highlightthickness=0)

    Inner = Tk.Frame(Canvas, bg=Bg_Panel)
    Inner.bind("<Configure>", lambda E: Canvas.configure(scrollregion=Canvas.bbox("all")))
    Canvas.create_window((0, 0), window=Inner, anchor="nw", tags="Inner_Frame")

    Canvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)
    Canvas.bind("<Configure>", lambda E: Canvas.itemconfig("Inner_Frame", width=E.width))

    return Inner

def Parse_Float(String_Val):
    if not String_Val: return 0.0
    return float(String_Val)

def Parse_Int(String_Val):
    if not String_Val: return 0
    return int(String_Val)

def Draw_Rounded_Rect(Canvas, X1, Y1, X2, Y2, Radius=12, **Kw):
    Points = [
        X1 + Radius, Y1,
        X2 - Radius, Y1,
        X2, Y1,
        X2, Y1 + Radius,
        X2, Y2 - Radius,
        X2, Y2,
        X2 - Radius, Y2,
        X1 + Radius, Y2,
        X1, Y2,
        X1, Y2 - Radius,
        X1, Y1 + Radius,
        X1, Y1,
    ]
    return Canvas.create_polygon(Points, smooth=True, **Kw)
