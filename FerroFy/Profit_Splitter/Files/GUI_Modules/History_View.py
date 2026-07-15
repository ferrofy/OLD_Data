import tkinter as Tk
from tkinter import ttk as Ttk
from Files.GUI_Modules.Constants import *
from Files.GUI_Modules.Utils import Bind_Hover

class History_Overlay:
    def __init__(self, App):
        self.App = App

    def Show(self):
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.destroy()

        self.Overlay_Frame = Tk.Frame(
            self.App.Root, bg=Bg_Panel,
            highlightbackground=Accent_Cyan_Dark, highlightthickness=2,
        )
        self.Overlay_Frame.place(relx=0.06, rely=0.06, relwidth=0.88, relheight=0.88)

        Tk.Frame(self.Overlay_Frame, bg=Accent_Cyan_Dark, height=3).pack(fill=Tk.X)

        Top_Bar = Tk.Frame(self.Overlay_Frame, bg=Bg_Panel)
        Top_Bar.pack(fill=Tk.X, pady=10, padx=18)

        Back_Btn = Tk.Button(
            Top_Bar, text="\u2b05  Back", bg=Bg_Card, fg=Accent_Cyan,
            font=("Segoe UI", 12, "bold"), borderwidth=0, cursor="hand2",
            command=self.Hide, activebackground=Accent_Cyan_Dark,
        )
        Back_Btn.pack(side=Tk.LEFT, ipadx=16, ipady=7)
        Bind_Hover(Back_Btn, Bg_Card, Border_Glow, Accent_Cyan, Accent_Gold_Light)

        Tk.Label(Top_Bar, text="\U0001f4cb  Balance History Log", bg=Bg_Panel, fg=Accent_Cyan,
                 font=("Segoe UI", 18, "bold")).pack(side=Tk.LEFT, padx=20)

        Tk.Frame(self.Overlay_Frame, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=18, pady=2)

        History = self.App.Dm.History
        Vals    = self.App.Dm.Get_Hist_Balances()
        Keys    = list(History.keys())

        Stats_Row = Tk.Frame(self.Overlay_Frame, bg=Bg_Main)
        Stats_Row.pack(fill=Tk.X, padx=20, pady=(10, 6))

        Total_Days = len(Keys)
        Latest_Bal = Vals[-1]  if Vals else 0.0
        Peak_Bal   = max(Vals) if Vals else 0.0
        Low_Bal    = min(Vals) if Vals else 0.0

        for Title, Val, Clr in [
            ("Recorded Days",   str(Total_Days),         Accent_Cyan),
            ("Latest Balance",  f"\u20b9{Latest_Bal:,.2f}", Accent_Gold),
            ("All-Time Peak",   f"\u20b9{Peak_Bal:,.2f}",   Accent_Green),
            ("All-Time Low",    f"\u20b9{Low_Bal:,.2f}",    Accent_Red),
        ]:
            F = Tk.Frame(Stats_Row, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
            F.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True, padx=5)
            Tk.Frame(F, bg=Clr, height=2).pack(fill=Tk.X)
            Tk.Label(F, text=Title, bg=Bg_Card, fg=Txt_Muted,  font=("Segoe UI", 9),       pady=6).pack()
            Tk.Label(F, text=Val,   bg=Bg_Card, fg=Clr,        font=("Segoe UI", 14, "bold"), pady=2).pack()
            Tk.Label(F, text="",    bg=Bg_Card,                                              pady=4).pack()

        Tk.Frame(self.Overlay_Frame, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=18, pady=4)

        Style = Ttk.Style()
        Style.theme_use("default")
        Style.configure(
            "History.Treeview",
            background=Bg_Card,
            foreground=Txt_Color,
            fieldbackground=Bg_Card,
            rowheight=38,
            font=("Segoe UI", 12),
            borderwidth=0,
        )
        Style.configure(
            "History.Treeview.Heading",
            background=Bg_Main,
            foreground=Accent_Cyan,
            font=("Segoe UI", 13, "bold"),
            borderwidth=0,
            relief="flat",
        )
        Style.map("History.Treeview",
            background=[("selected", Glow_Cyan)],
            foreground=[("selected", Accent_Cyan)],
        )

        Tree_Frame = Tk.Frame(self.Overlay_Frame, bg=Bg_Main)
        Tree_Frame.pack(fill=Tk.BOTH, expand=True, padx=20, pady=(0, 18))

        Columns = ("No", "Date", "Balance", "Change", "Change %", "Trend")
        Tree = Ttk.Treeview(Tree_Frame, columns=Columns, show="headings", style="History.Treeview")

        V_Scroll = Ttk.Scrollbar(Tree_Frame, orient="vertical", command=Tree.yview)
        V_Scroll.pack(side=Tk.RIGHT, fill=Tk.Y)
        Tree.configure(yscrollcommand=V_Scroll.set)

        for Col, W, Anchor in [
            ("No",       55,  "center"),
            ("Date",     200, "center"),
            ("Balance",  200, "center"),
            ("Change",   170, "center"),
            ("Change %", 130, "center"),
            ("Trend",    100, "center"),
        ]:
            Tree.heading(Col, text=Col)
            Tree.column(Col, anchor=Anchor, width=W, stretch=Col == "Balance")

        Tree.tag_configure("pos",  foreground=Accent_Green)
        Tree.tag_configure("neg",  foreground=Accent_Red)
        Tree.tag_configure("flat", foreground=Txt_Muted)

        for I, (Date_Key, Raw_Entry) in enumerate(reversed(list(History.items()))):
            Idx        = Total_Days - I
            Rev_Idx    = Total_Days - 1 - I
            Entry      = self.App.Dm._Normalize_Entry(Raw_Entry)
            Balance    = Entry.get("b", 0.0)
            Prev_Bal   = Vals[Rev_Idx - 1] if Rev_Idx > 0 else Balance
            Delta      = Balance - Prev_Bal
            Pct        = ((Delta / abs(Prev_Bal)) * 100) if Prev_Bal != 0 and Rev_Idx > 0 else 0.0
            Sign       = "+" if Delta >= 0 else ""
            Trend      = "\u25b2 Up" if Delta > 0 else ("\u25bc Down" if Delta < 0 else "\u2014 Flat")
            Tag        = "pos" if Delta > 0 else ("neg" if Delta < 0 else "flat")
            Delta_Str  = f"{Sign}\u20b9{Delta:,.2f}" if Rev_Idx > 0 else "\u2014"
            Pct_Str    = f"{Sign}{Pct:.2f}%"         if Rev_Idx > 0 else "\u2014"

            Tree.insert("", Tk.END,
                        values=(Idx, Date_Key, f"\u20b9{Balance:,.2f}", Delta_Str, Pct_Str, Trend),
                        tags=(Tag,))

        Tree.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

        Tree.bind("<MouseWheel>", lambda E: Tree.yview_scroll(int(-1 * E.delta / 120), "units"))

    def Hide(self):
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.place_forget()
            self.Overlay_Frame.destroy()
