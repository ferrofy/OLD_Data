import tkinter as Tk
from Files.GUI_Modules.Constants import (
    Bg_Panel, Bg_Card, Bg_Main, Border_Glow, Border_Color,
    Accent_Gold, Accent_Gold_Dark, Accent_Gold_Light, Accent_Green, Accent_Red,
    Accent_Cyan, Accent_Purple,
    Glow_Gold, Txt_Color, Txt_Muted,
)

Group_Colors = [
    "#FF6B6B", "#4ECDC4", "#FFD93D", "#6BCB77",
    "#FF8B94", "#C7B8EA", "#74C0FC", "#FFD700",
    "#FFA07A", "#B0E0E6", "#DDA0DD", "#98FB98",
]

Group_Glow_Colors = [
    "#3D0000", "#003D3A", "#3D3300", "#003D1A",
    "#3D1A1A", "#1E1A3D", "#001A3D", "#3D3000",
    "#3D1E0A", "#0A2A2F", "#2A1A2A", "#0A2A1A",
]

def Build_Balance_Panel(Gui_Ref, Parent):
    Tk.Frame(Parent, bg=Accent_Gold_Dark, height=3).pack(fill=Tk.X)

    Header_Row = Tk.Frame(Parent, bg=Bg_Panel)
    Header_Row.pack(fill=Tk.X, padx=14, pady=(10, 4))

    Tk.Label(Header_Row, text="💼", font=("Segoe UI", 17), bg=Bg_Panel, fg=Accent_Gold).pack(side=Tk.LEFT)
    Tk.Label(Header_Row, text="  Portfolio", font=("Segoe UI", 15, "bold"), bg=Bg_Panel, fg=Accent_Gold).pack(side=Tk.LEFT)

    Gui_Ref.Total_Hero = Tk.Frame(Parent, bg=Glow_Gold, highlightbackground=Accent_Gold_Dark, highlightthickness=1)
    Gui_Ref.Total_Hero.pack(fill=Tk.X, padx=10, pady=(0, 6))
    Tk.Frame(Gui_Ref.Total_Hero, bg=Accent_Gold, height=2).pack(fill=Tk.X)

    Sub_Row = Tk.Frame(Gui_Ref.Total_Hero, bg=Glow_Gold)
    Sub_Row.pack(fill=Tk.X, padx=14, pady=(6, 2))
    Tk.Label(Sub_Row, text="Total Balance", bg=Glow_Gold, fg=Txt_Muted, font=("Segoe UI", 10)).pack(side=Tk.LEFT)
    Tk.Label(Sub_Row, text="PORTFOLIO", bg=Glow_Gold, fg=Accent_Gold_Dark, font=("Segoe UI", 8, "bold")).pack(side=Tk.RIGHT)

    Gui_Ref.Total_Val_Label = Tk.Label(
        Gui_Ref.Total_Hero, text="₹0.00", bg=Glow_Gold, fg=Accent_Gold,
        font=("Segoe UI", 26, "bold")
    )
    Gui_Ref.Total_Val_Label.pack(pady=(2, 8))

    Tk.Frame(Parent, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=10, pady=2)

    Gui_Ref.Bal_Canvas = Tk.Canvas(Parent, bg=Bg_Panel, bd=0, highlightthickness=0)
    Gui_Ref.Bal_Scroll = Tk.Scrollbar(Parent, orient=Tk.VERTICAL, command=Gui_Ref.Bal_Canvas.yview)

    Gui_Ref.Bal_Canvas.pack(fill=Tk.BOTH, expand=True, padx=6, pady=4)
    Gui_Ref.Bal_Canvas.configure(yscrollcommand=Gui_Ref.Bal_Scroll.set)

    Gui_Ref.Bal_Inner = Tk.Frame(Gui_Ref.Bal_Canvas, bg=Bg_Panel)
    Gui_Ref._Bal_Win  = Gui_Ref.Bal_Canvas.create_window((0, 0), window=Gui_Ref.Bal_Inner, anchor="nw")

    Gui_Ref.Bal_Inner.bind("<Configure>", lambda E: Gui_Ref.Bal_Canvas.configure(scrollregion=Gui_Ref.Bal_Canvas.bbox("all")))
    Gui_Ref.Bal_Canvas.bind("<Configure>", lambda E: Gui_Ref.Bal_Canvas.itemconfig(Gui_Ref._Bal_Win, width=E.width))
    Gui_Ref.Bal_Canvas.bind("<MouseWheel>", lambda E: Gui_Ref.Bal_Canvas.yview_scroll(int(-1 * E.delta / 120), "units"))

def Update_Balance_Display(Gui_Ref):
    for W in Gui_Ref.Bal_Inner.winfo_children():
        W.destroy()

    Total = 0.0
    for Item in Gui_Ref.Dm.Savings:
        if isinstance(Item, list):
            Total += float(Item[1])

    Total_Clr = Accent_Green if Total >= 0 else Accent_Red
    Gui_Ref.Total_Val_Label.config(text=f"₹{Total:,.2f}", fg=Total_Clr)
    Gui_Ref.Total_Hero.config(bg=Glow_Gold)
    Gui_Ref.Total_Val_Label.config(bg=Glow_Gold)

    Count     = 0
    Group_Idx = -1
    for Item in Gui_Ref.Dm.Savings:
        if isinstance(Item, str):
            Group_Idx += 1
            Grp_Color  = Group_Colors[Group_Idx % len(Group_Colors)]
            Grp_Glow   = Group_Glow_Colors[Group_Idx % len(Group_Glow_Colors)]

            Lbl_Row = Tk.Frame(Gui_Ref.Bal_Inner, bg=Grp_Glow, highlightbackground=Grp_Color, highlightthickness=1)
            Lbl_Row.pack(fill=Tk.X, padx=6, pady=(10, 0))

            Tk.Frame(Lbl_Row, bg=Grp_Color, width=4).pack(side=Tk.LEFT, fill=Tk.Y)
            Inner_Label = Tk.Frame(Lbl_Row, bg=Grp_Glow)
            Inner_Label.pack(side=Tk.LEFT, fill=Tk.X, expand=True, padx=8, pady=4)
            Tk.Label(Inner_Label, text=f"  {Item.upper()}", bg=Grp_Glow, fg=Grp_Color, font=("Segoe UI", 10, "bold")).pack(side=Tk.LEFT)

        elif isinstance(Item, list):
            Count     += 1
            Name       = Item[0].strip()
            Amount     = float(Item[1])
            Grp_Color  = Group_Colors[Group_Idx % len(Group_Colors)] if Group_Idx >= 0 else Accent_Gold
            Amt_Clr    = Accent_Green if Amount >= 0 else Accent_Red
            Sign       = "▲" if Amount >= 0 else "▼"

            Card = Tk.Frame(Gui_Ref.Bal_Inner, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
            Card.pack(fill=Tk.X, padx=6, pady=1)

            Accent_Strip = Tk.Frame(Card, bg=Grp_Color, width=3)
            Accent_Strip.pack(side=Tk.LEFT, fill=Tk.Y)

            Inner_Row = Tk.Frame(Card, bg=Bg_Card)
            Inner_Row.pack(fill=Tk.X, padx=8, pady=6)

            Num_Lbl = Tk.Label(Inner_Row, text=f"{Count}.", bg=Bg_Card, fg=Txt_Muted, font=("Segoe UI", 9), width=3, anchor="e")
            Num_Lbl.pack(side=Tk.LEFT)

            Name_Lbl = Tk.Label(Inner_Row, text=Name, bg=Bg_Card, fg=Txt_Color, font=("Segoe UI", 11), anchor="w")
            Name_Lbl.pack(side=Tk.LEFT, fill=Tk.X, expand=True, padx=(4, 0))

            Amt_Lbl = Tk.Label(Inner_Row, text=f"{Sign} ₹{Amount:,.2f}", bg=Bg_Card, fg=Amt_Clr, font=("Segoe UI", 11, "bold"), anchor="e")
            Amt_Lbl.pack(side=Tk.RIGHT)

            _Bind_Card_Hover(Card, Inner_Row, Name_Lbl, Num_Lbl, Amt_Lbl, Accent_Strip, Grp_Color)

    Tk.Frame(Gui_Ref.Bal_Inner, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=8, pady=8)
    _Bind_Bal_Scroll(Gui_Ref, Gui_Ref.Bal_Inner)

def _Bind_Card_Hover(Card, Inner_Row, Name_Lbl, Num_Lbl, Amt_Lbl, Strip, Grp_Color):
    Hover_Bg = "#1A1A2E"

    def On_Enter(E):
        Card.config(bg=Hover_Bg, highlightbackground=Grp_Color)
        Inner_Row.config(bg=Hover_Bg)
        Name_Lbl.config(bg=Hover_Bg)
        Num_Lbl.config(bg=Hover_Bg)
        Amt_Lbl.config(bg=Hover_Bg)

    def On_Leave(E):
        from Files.GUI_Modules.Constants import Bg_Card, Border_Glow
        Card.config(bg=Bg_Card, highlightbackground=Border_Glow)
        Inner_Row.config(bg=Bg_Card)
        Name_Lbl.config(bg=Bg_Card)
        Num_Lbl.config(bg=Bg_Card)
        Amt_Lbl.config(bg=Bg_Card)

    for W in [Card, Inner_Row, Name_Lbl, Num_Lbl, Amt_Lbl, Strip]:
        W.bind("<Enter>", On_Enter)
        W.bind("<Leave>", On_Leave)

def _Scroll_Bal(Gui_Ref, E):
    Gui_Ref.Bal_Canvas.yview_scroll(int(-1 * E.delta / 120), "units")

def _Bind_Bal_Scroll(Gui_Ref, Widget):
    Widget.bind("<MouseWheel>", lambda E: _Scroll_Bal(Gui_Ref, E))
    for Child in Widget.winfo_children():
        _Bind_Bal_Scroll(Gui_Ref, Child)
